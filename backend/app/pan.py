import httpx
from fastapi import APIRouter
from fastapi import Request, Depends
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.auth.utils import get_current_user, TokenData
from app.database import get_db, update_analytics
from app.schemas import PanCardResponse
from app.utils import BASE_URI, get_headers

PAN_VALIDATION_PRODUCT_ID = "289ca52c-361a-48d7-9090-de8ab8bd3c52"

router = APIRouter()

class PanVerificationRequest(BaseModel):
    pan: str
    consent: str 
    reason: str

@router.post("/api/verify/pan")
async def validate_pan(pan_request: PanVerificationRequest, request: Request, current_user: TokenData = Depends(get_current_user)):
    request_path = request.url.path
    headers = get_headers(PAN_VALIDATION_PRODUCT_ID)
    payload = pan_request.dict()
    url = get_url(request_path)
    print('pan validation url:', url)

    async with httpx.AsyncClient() as client:
        response = await client.post(url, json=payload, headers=headers)
        print('got response:', response.json())

    if 200 <= response.status_code < 300:
        return success_response(response.json())
    else:
        return update_analytics(response.json(), response.status_code, current_user.username)

def get_url(request_path):
    return BASE_URI + request_path

def success_response(response) -> PanCardResponse:
    verification = (response.get("verification","N/A")).lower()
    if verification == "success":
        data = response.get('data',{})
        full_name = data.get("full_name", "N/A")
        aadhaar_seeding_status = data.get("aadhaar_seeding_status", "N/A")
        message = response.get("message", "PAN is valid")
        
        if aadhaar_seeding_status == "LINKED":
            return PanCardResponse(status = 200, message=message, full_name = full_name)
        else:
            message = "Aadhar status should be LINKED."
            return PanCardResponse(status=401, message=message)
    else:
        return PanCardResponse(status =401, message = "Pan is invalid, please retry")

def update_analytics(response, status_code, username, db: Session = Depends(get_db)):
    error = response.get("error", {})
    details = error.get("detail","n/a")
    trace_id = error.get("traceId","N/a")
    update_analytics('kyc_fail', username, db) # can we do this in async way ?
    return JSONResponse(status_code=status_code, content={"message": details, "traceId": trace_id})
