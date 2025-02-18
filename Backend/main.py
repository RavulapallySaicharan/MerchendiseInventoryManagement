from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel, EmailStr
from typing import Dict, Optional
from datetime import datetime, timedelta
from jose import JWTError, jwt
from passlib.context import CryptContext
import secrets

# Initialize FastAPI app
app = FastAPI()

# Security configurations
SECRET_KEY = "your-secret-key-here"  # In production, use environment variable
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# In-memory storage
users: Dict[str, dict] = {}
reset_tokens: Dict[str, str] = {}

# Pydantic models
class UserCreate(BaseModel):
    email: EmailStr
    username: str
    password: str

class User(BaseModel):
    email: EmailStr
    username: str
    is_active: bool = True

class Token(BaseModel):
    access_token: str
    token_type: str

class ResetPassword(BaseModel):
    email: EmailStr

class ChangePassword(BaseModel):
    token: str
    new_password: str

# Helper functions
def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

# API endpoints
@app.post("/register", response_model=User)
def register_user(user: UserCreate):
    if user.email in users:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    hashed_password = get_password_hash(user.password)
    users[user.email] = {
        "username": user.username,
        "hashed_password": hashed_password,
        "is_active": True
    }
    
    return User(email=user.email, username=user.username)

@app.post("/token", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user_data = users.get(form_data.username)
    if not user_data or not verify_password(form_data.password, user_data["hashed_password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": form_data.username},
        expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@app.post("/reset-password")
def request_password_reset(reset_request: ResetPassword):
    if reset_request.email not in users:
        raise HTTPException(status_code=404, detail="User not found")
    
    reset_token = secrets.token_urlsafe(32)
    reset_tokens[reset_token] = reset_request.email
    
    # In a real application, send this token via email
    return {"message": "Password reset link has been sent to your email", "token": reset_token}

@app.post("/change-password")
def change_password(change_request: ChangePassword):
    if change_request.token not in reset_tokens:
        raise HTTPException(status_code=400, detail="Invalid or expired reset token")
    
    email = reset_tokens[change_request.token]
    users[email]["hashed_password"] = get_password_hash(change_request.new_password)
    del reset_tokens[change_request.token]
    
    return {"message": "Password has been successfully changed"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
