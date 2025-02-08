from typing import Optional

from app.auth.utils import get_password_hash, verify_password, create_access_token, TokenData, get_current_user, \
    get_new_access_token, create_refresh_token
from app.database import init_db, get_db, User, update_analytics, get_analytics_data
from app.pan import router as pan_verification_router
from app.rpd import router as rpd_router
from app.services import register_user, login_user, fetch_refresh_token

from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI, Header, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.security import HTTPBasic, HTTPBasicCredentials

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.schemas import LoginResponseDto, UserCreateDto, UserResponseDto, RegisterResponseDto, TokenRefreshResponseDto, RefreshAccessTokenRequest

import uvicorn


@asynccontextmanager
async def lifespan(app_: FastAPI):
    print("Server is starting...")
    yield
    print("server is stopping")


app = FastAPI(lifespan=lifespan)
app.include_router(pan_verification_router)
app.include_router(rpd_router)
security = HTTPBasic()
init_db()

origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "http://localhost:4173",
    "http://127.0.0.1:4173",
    "http://setufrontend:4173",
    "http://157.245.105.144:4173",
    "http://172.31.0.4:4173",
    "http://167.71.234.205:4173",
    "http://setufrontend:3000",
    "http://172.31.0.4:3000",
    "http://157.245.105.144:4173",
    "https://*.ngrok-free.app",
    "https://*.ngrok.io"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
    allow_origin_regex=r"https://.*\.ngrok-free\.app"
)


def get_user_by_username(db: Session, username: str) -> User:
    return db.query(User).filter(User.username == username).first()


@app.post("/register")
def register(user: UserCreateDto, db: Session = Depends(get_db)) -> RegisterResponseDto:
    db_user = get_user_by_username(db, user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    return register_user(user, db)


@app.post("/login")
def login(credentials: HTTPBasicCredentials = Depends(security), db: Session = Depends(get_db)) -> LoginResponseDto:
    user = get_user_by_username(db, credentials.username)
    if not user or not verify_password(credentials.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Basic"})
    return login_user(credentials.username)

@app.post("/refresh")
def refresh_token(dto: RefreshAccessTokenRequest) -> TokenRefreshResponseDto:
    return fetch_refresh_token(dto.username, dto.refresh_token)

@app.post("/logout")
def logout(db: Session = Depends(get_db)):
    pass


@app.get("/")
def read_root(accept: str = Header(None),user_agent: str = Header(None), username: Optional[str] = "User"):
    request_headers = {"Accept": accept, "User-Agent": user_agent}
    return {"message": f"Welcome to the KYC Module API submission by {username}!",
            "request_headers": request_headers}


@app.get("/update-analytics/{username}")
def success(username: str, db: Session = Depends(get_db), current_user: TokenData = Depends(get_current_user)):
    update_analytics('pass', username, db)


@app.get("/analyticsdata")
def get_analytics(current_user: TokenData = Depends(get_current_user), db: Session = Depends(get_db)):
    analytics_data = get_analytics_data(db)
    if current_user.username != "admin":
        return JSONResponse(status_code=401, content={"message": "forbidden"})
    return analytics_data


if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
