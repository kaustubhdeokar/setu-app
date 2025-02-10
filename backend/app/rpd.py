from asyncio import Event, wait_for
from typing import Dict, Optional

import httpx
import requests
from fastapi import APIRouter, HTTPException, Request, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from app.auth.utils import get_current_user, TokenData
from app.analytics import update_analytics_table
from app.schemas import RequestModel
from app.utils import BASE_URI, get_headers
from app.database import get_db

BANK_FLOW_FAIL = 'bank_fail'
BANK_FLOW_PASS = 'bank_pass'

router = APIRouter()

class WebhookManager:
    def __init__(self):
        self.future_events: Dict[str, Event] = {}
        self.responses: Dict[str, dict] = {}

    def create_event(self, request_id: str) -> Event:
        print('creating event for id:', request_id)
        self.future_events[request_id] = Event()
        return self.future_events[request_id]

    def set_response(self, request_id: str, data: dict):
        self.responses[request_id] = data
        print('setting response for id:', request_id)
        if request_id in self.future_events:
            self.future_events[request_id].set()

    def get_response(self, request_id: str) -> Optional[dict]:
        print('getting response for id:', request_id)
        return self.responses.get(request_id)

    def cleanup(self, request_id: str):
        self.future_events.pop(request_id, None)
        self.responses.pop(request_id, None)


webhook_manager = WebhookManager()
headers = get_headers("e044e23a-720e-4897-8080-1c6bb3a48794")


@router.post("/api/verify/ban/reverse/webhook")
async def webhook_listener(webhook_response: Request):
    try:
        data = await webhook_response.json()
        print("Received Webhook Data:", data)
        request_id = data.get("data").get("rpd", {}).get("id", {})
        if not request_id:
            raise HTTPException(status_code=400, detail="Missing requestId")

        account_info = extract_account_info(data)
        webhook_manager.set_response(request_id, account_info)
        return {"status": "success"}

    except Exception as e:
        print(f"Error processing webhook: {str(e)}")
        raise HTTPException(status_code=500, detail={"error": str(e)})


def extract_account_info(data):
    data = data.get("data", {}).get("rpd", {}).get("data", {})
    return {
        "bank_account": data.get("bankAccountNumber", ''),
        "ifsc": data.get("bankAccountIfsc", '')
    }


@router.get("/api/verify/ban/reverse/{request_id}")
async def get_details(request_id: str, request: Request):
    # return fake_response()
    request_path = request.url.path
    url = BASE_URI + request_path
    print('url: %s' % url)
    response = requests.get(url, headers=headers).json()
    payload = create_details_payload(response)
    return JSONResponse(status_code=200, content=payload)


def create_details_payload(response):
    data = response.get("data", {})
    bank_account = data.get("bankAccountNumber", {})
    ifsc = data.get("bankAccountIfsc")
    return {
        "bank_account": bank_account,
        "ifsc": ifsc
    }


@router.post("/api/verify/ban/reverse")
async def validate_rpd(request: Request, current_user: TokenData = Depends(get_current_user)):
    request_model = RequestModel()
    return await validate_rpd(request_model, request, current_user)


@router.post("/api/verify/ban/reverse")
async def validate_rpd(request_model: RequestModel, request: Request,
                       current_user: TokenData = Depends(get_current_user)):
    async with httpx.AsyncClient() as client:
        # return fake_response()
        print('username',current_user.username)
        payload = create_payload(request_model)
        request_path = request.url.path
        url = get_rpd_url(request_path)
        response = await client.post(url, json=payload, headers=headers)
        print('response received from rpd', response.json())
        request_id = extract_request_id(response.json())
        print('request_id = %s' % request_id)
        if not request_id:
            update_analytics(BANK_FLOW_FAIL, response.json(), response.status_code, current_user.username)
            raise HTTPException(status_code=400, detail="Failed to get request ID")

        ## Mock payment.
        event = webhook_manager.create_event(request_id)
        url = get_mock_payment_url(BASE_URI, request_path, request_id)
        mock_payment_response = await client.post(url, headers=headers)
        mock_payment_response.raise_for_status()
        print('response received from rpd', mock_payment_response.json())

        ### waiting for response from webhook.
        try:
            await wait_for(event.wait(), timeout=40.0)  # 40 seconds timeout
            webhook_data = webhook_manager.get_response(request_id)
            print('response received:', webhook_data)
            if not webhook_data:
                raise HTTPException(status_code=500, detail="Webhook data not received")
            payload = create_payload_from_webhook(webhook_data, request_id)
            update_analytics(BANK_FLOW_PASS, response.json(), response.status_code, current_user.username)
            return JSONResponse(status_code=200, content=payload)
        except TimeoutError:
            return update_analytics(BANK_FLOW_FAIL, response.json(), response.status_code, current_user.username)
        finally:
            webhook_manager.cleanup(request_id)


def update_analytics(case: str, response: dict, status_code: int, username: str):
    error = response.get("error", {})
    details = error.get("detail", "n/a")
    trace_id = error.get("traceId", "N/a")
    db = next(get_db())
    update_analytics_table(case, username, db)
    return JSONResponse(status_code=status_code, content={"message": details, "traceId": trace_id})


def create_payload_from_webhook(webhook_data, request_id):
    bank_account = webhook_data["bank_account"]
    ifsc = webhook_data["ifsc"]
    return {
        "request_id": request_id,
        "bank_account": bank_account,
        "ifsc": ifsc,
        "status": 200
    }


def get_mock_payment_url(base_url, request_path, request_id):
    return base_url + request_path + '/mock_payment/' + request_id


def extract_request_id(response):
    return response.get("id", "N/A")


def get_rpd_url(request_path):
    return BASE_URI + request_path


def create_payload(request_model: RequestModel):
    return {
        "redirectionConfig": {
            "redirectUrl": request_model.redirectionConfig.redirectUrl,
            "timeout": request_model.redirectionConfig.timeout
        } if request_model.redirectionConfig else {},
        "additionalData": request_model.additionalData if request_model.additionalData else {}
    }


def fake_response():
    return JSONResponse(status_code=200, content={
        "request_id": "aa99d6ad-1ea4-4d03-9f41-1849d5d1f319",
        "bank_account": "9009120939129",
        "ifsc": "SBIN0000539",
        "status": 200
    })
