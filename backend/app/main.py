from fastapi import FastAPI, Depends, HTTPException, status, Request, Response
from app.pan import router as pan_verification_router
from app.rpd import router as rpd_router
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from pydantic import BaseModel, ValidationError
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
import uvicorn
from app.auth.utils import get_password_hash, verify_password, create_access_token, TokenData, get_current_user
from app.database import init_db, get_db, User, update_analytics, get_analytics_data
from fastapi.responses import JSONResponse


app = FastAPI()
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
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
    allow_origin_regex=r"https://.*\.ngrok-free\.app"
)


class UserCreate(BaseModel):
    username: str
    password: str
    pan_number:str
    
@app.options("/login")
async def options_handler(response: Response):
    print("Received OPTIONS request")
    return {"status": "ok"}

@app.options("/register")
async def options_handler(response: Response):
    print("Received OPTIONS request")
    return {"status": "ok"}

@app.post("/register", response_model=dict)
def register(user: UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.username == user.username).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    hashed_password = get_password_hash(user.password)
    new_user = User(username=user.username, hashed_password=hashed_password, pan_number=user.pan_number)
    try:
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="PAN number already registered")
    return JSONResponse(status_code=200, content=
{"status":200, "message": "User registered successfully"})

@app.post("/login")
def login(credentials: HTTPBasicCredentials = Depends(security), db: Session = Depends(get_db)):
    print(credentials.username+":"+credentials.password)
    user = db.query(User).filter(User.username == credentials.username).first()
    if not user or not verify_password(credentials.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Basic"},
        )
    return JSONResponse(status_code=200, content= 
    {"status":200, "user":user.username, "token":create_access_token(data={"sub": user.username})})


@app.get("/")
def read_root():
    return {"message": "Welcome to the KYC Module API submission by Kaustubh !"}

@app.get("/update-analytics/{username}")
def success(username:str,db: Session = Depends(get_db),current_user: TokenData = Depends(get_current_user)):
    update_analytics('pass',username,db)

@app.get("/analyticsdata")
def get_analytics(current_user: TokenData = Depends(get_current_user), db: Session = Depends(get_db)):
    analytics_data = get_analytics_data(db)
    if current_user.username != "admin":
        return JSONResponse(status_code=401, content= {"message": "forbidden"})
    return analytics_data

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)