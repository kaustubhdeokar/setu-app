from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from fastapi import APIRouter, HTTPException
import requests
from typing import Dict, Any
import httpx
from app.utils import BASE_URI, POSTMAN_LOCAL_SERVER_URL, SANDBOX_API_URL

router = APIRouter()

class PanVerificationRequest(BaseModel):
    pan: str
    consent: str 
    reason: str

@router.post("/api/verify/pan")
def validate_pan(pan_request: PanVerificationRequest, request: Request):
    request_path = request.url.path
    print(f"Request path: {request_path}")
    headers = {
        "Content-Type": "application/json",
        "x-client-id":"b79b7d73-1c17-43f5-8c4c-8c185765c1c1",
        "x-client-secret":"jHlqATEpLKo4OXgF28gjFOdOT4Nk06Vo",
        "x-product-instance-id":"289ca52c-361a-48d7-9090-de8ab8bd3c52"
    }
    payload = pan_request.dict()
    
    url = get_url(BASE_URI , request_path)
    print('url:', url)
    response = requests.post(url, json=payload, headers=headers)
    print('response:', response.json())

    if response.status_code == 200:
        return success_response(response.json())
    elif response.status_code == 400:
        return bad_request(response.json())
    else:
        return internal_server_error(response.json())

def get_url(base_url, request_path):
    return BASE_URI + request_path

def success_response(response):
    verification = (response.get("verification","N/A")).lower()
    if verification == "success":
        data = response.get('data',{})
        full_name = data.get("full_name", "N/A")
        aadhaar_seeding_status = data.get("aadhaar_seeding_status", "N/A")
        message = response.get("message", "PAN is valid")
        
        if aadhaar_seeding_status == "LINKED":
            return JSONResponse(status_code=200, content={"message": message,
                "full_name": full_name, "status":200})
        else:
            return JSONResponse(status_code=401, content={"verification": "failed", 
                "message": "Aadhar status should be LINKED.", "status":401})
    else:
        return JSONResponse(status_code=401, 
                content={"verification": "failed", "message": "pan is invalid", "status":401})

def bad_request(response):
    error = response.get("error", {})
    details = error.get("detail","n/a")
    trace_id = error.get("traceId","N/a")
    return JSONResponse(status_code=400, content={"message": details, "traceId": trace_id})

def internal_server_error(response: Dict[str, Any]):
    error = response.get("error", {})
    details = error.get("detail","n/a")
    trace_id = error.get("traceId","N/a")
    return JSONResponse(status_code=500, content={"message": error, "traceId": trace_id})