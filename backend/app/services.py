from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.auth.utils import get_password_hash, create_access_token, create_refresh_token
from app.models import User
from app.schemas import LoginResponseDto, UserCreateDto, UserResponseDto, RegisterResponseDto, TokenRefreshResponseDto

from app.auth.utils import get_new_access_token

def register_user(user: UserCreateDto, db: Session) -> RegisterResponseDto:

    hashed_password = get_password_hash(user.password)
    new_user = User(username=user.username, hashed_password=hashed_password, pan_number=user.pan_number)

    try:
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="PAN number already registered")

    user_response = UserResponseDto(username=user.username, pan_number=user.pan_number)
    return RegisterResponseDto(status=200, message="User registered successfully", user=user_response)

def login_user(username: str) -> LoginResponseDto:
    access_token = create_access_token(data={"sub": username})
    refresh_token = create_refresh_token(data={"sub": username})
    return LoginResponseDto(status=200, message=f"{username} is logged in",
                            access_token = access_token,
                            refresh_token = refresh_token)

def fetch_refresh_token(username: str, refresh_token_: str) -> TokenRefreshResponseDto:
    access_token = get_new_access_token(username, refresh_token_)
    return TokenRefreshResponseDto(status=200, message=f"token refreshed {access_token}", token=access_token)

