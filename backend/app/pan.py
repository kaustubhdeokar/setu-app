import httpx
from fastapi import APIRouter
from fastapi import Request, Depends
from pydantic import BaseModel

from app.auth.utils import get_current_user, TokenData
from app.database import get_db
from app.analytics import update_analytics_table
from app.schemas import PanCardResponse
from app.utils import BASE_URI, get_headers
from sqlalchemy.orm import Session

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
    db = get_db()
    if 200 <= response.status_code < 300:
        return validate_response(response.json(), current_user.username, db)
    else:
        msg = update_analytics_fail(response.json(), current_user.username)
        return PanCardResponse(status=401, message=msg)

def get_url(request_path):
    return BASE_URI + request_path

def validate_response(response, username, db: Session) -> PanCardResponse:
    verification = (response.get("verification","N/A")).lower()
    if verification == "success":
        data = response.get('data',{})
        full_name = data.get("full_name", "N/A")
        aadhaar_seeding_status = data.get("aadhaar_seeding_status", "N/A")
        message = response.get("message")
        
        if aadhaar_seeding_status == "LINKED":
            update_analytics_pass(username)
            return PanCardResponse(status = 200, message=message, full_name = full_name)
        else:
            message = "Aadhar status should be LINKED."
            update_analytics_fail(response.json(), username)
            return PanCardResponse(status=401, message=message)
    else:
        update_analytics_fail(response, username)
        return PanCardResponse(status =401, message = response.get("message"))

def update_analytics_fail(response: dict, username:str) -> []:
    error = response.get("error", {})
    details = error.get("detail","n/a")
    trace_id = error.get("traceId","N/a")
    db = next(get_db())
    update_analytics_table('kyc_fail', username, db)
    return {details, trace_id}

# db: Session = Depends(get_db)):
def update_analytics_pass(username:str):
    db = next(get_db())
    update_analytics_table('kyc_pass', username, db)