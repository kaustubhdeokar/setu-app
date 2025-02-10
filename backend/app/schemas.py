from pydantic import BaseModel
from typing import Optional
from typing import Dict, Any, Optional

class UserCreateDto(BaseModel):
    username: str
    password: str
    pan_number: str

class UserResponseDto(BaseModel):
    username: str
    pan_number: str

class RegisterResponseDto(BaseModel):
    status: int
    message: str
    user: UserResponseDto

class LoginResponseDto(BaseModel):
    status: int
    message: str
    access_token: str
    refresh_token: str

class TokenRefreshResponseDto(BaseModel):
    status: int
    message: str
    token: str

class PanCardResponse(BaseModel):
    status:int
    message:str
    full_name: Optional[str] = None


class AnalyticsResponse(BaseModel):
    id: int
    username: str
    pass_kyc: int
    fail_kyc: int
    pass_bank: int
    fail_bank: int
    total_pass: int
    total_fail: int

class RefreshAccessTokenRequest(BaseModel):
    username: str
    refresh_token:str

class RedirectionConfig(BaseModel):
    redirectUrl: str
    timeout: int

class RequestModel(BaseModel):
    redirectionConfig: Optional[RedirectionConfig] = None
    additionalData: Optional[Dict[str, Any]] = None

class TokenData(BaseModel):
    username: str
