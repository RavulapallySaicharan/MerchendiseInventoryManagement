from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel, EmailStr
from typing import Dict, Optional, List
from datetime import datetime, timedelta
from jose import JWTError, jwt
from passlib.context import CryptContext
import secrets
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from database import get_db
import models
from database import engine
from add_products import add_products
from models import Product
import smtplib
import asyncio
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import sqlite3

# Database and Email Configuration
DB_PATH = "app.db"
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
EMAIL_SENDER = "ravulapally.saicharan261@gmail.com"
EMAIL_PASSWORD = "CherryRavu1!"
EMAIL_RECEIVER = "ravulapally.saicharan261@gmail.com"

models.Base.metadata.create_all(bind=engine)
add_products()

# Initialize FastAPI app
app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# Security configurations
SECRET_KEY = "your-secret-key-here"  # In production, use environment variable
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

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

async def check_low_stock():
    """Checks for low stock products and sends email notifications every 3 Hours."""
    while True:
        try:
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()
            query = """SELECT name, stock_level, reorder_threshold FROM Products WHERE stock_level < reorder_threshold"""
            cursor.execute(query)
            low_stock_items = cursor.fetchall()
            conn.close()

            if low_stock_items:
                await send_email_notification(low_stock_items)
                print("Low stock alert email sent successfully.")

        except Exception as e:
            print(f"Error checking low stock: {e}")

        await asyncio.sleep(3600 * 3)  # Wait for 3 hours before checking again

async def send_email_notification(products):
    """Sends an email notification for low stock products."""
    try:
        subject = "Low Stock Alert 🚨"
        body = "The following products are low in stock:\n\n"

        for name, stock, threshold in products:
            body += f"- {name}: {stock} (Threshold: {threshold})\n"

        msg = MIMEMultipart()
        msg["From"] = EMAIL_SENDER
        msg["To"] = EMAIL_RECEIVER
        msg["Subject"] = subject
        msg.attach(MIMEText(body, "plain"))

        # Sending email
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(EMAIL_SENDER, EMAIL_PASSWORD)
        server.sendmail(EMAIL_SENDER, EMAIL_RECEIVER, msg.as_string())
        server.quit()

        print("Low stock alert email sent successfully.")

    except Exception as e:
        print(f"Error sending email: {e}")

# API endpoints
@app.on_event("startup")
async def start_background_task():
    """Starts the background task when FastAPI app starts."""
    asyncio.create_task(check_low_stock())

@app.post("/register", response_model=User)
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    hashed_password = get_password_hash(user.password)
    db_user = models.User(
        email=user.email,
        username=user.username,
        hashed_password=hashed_password
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@app.post("/token", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == form_data.username).first()
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@app.post("/reset-password")
def request_password_reset(reset_request: ResetPassword, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == reset_request.email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    reset_token = secrets.token_urlsafe(32)
    user.reset_token = reset_token
    db.commit()
    
    # In a real application, send this token via email
    return {"message": "Password reset link has been sent to your email", "token": reset_token}

@app.post("/change-password")
def change_password(change_request: ChangePassword, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.reset_token == change_request.token).first()
    if not user:
        raise HTTPException(status_code=400, detail="Invalid or expired reset token")
    
    user.hashed_password = get_password_hash(change_request.new_password)
    user.reset_token = None  # Clear the reset token
    db.commit()
    return {"message": "Password has been successfully changed"}


@app.get("/products")
def get_products(db: Session = Depends(get_db)):
    products = db.query(Product).all()
    return products

@app.get("/products/{product_name}")
def get_product(product_name: str, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.name == product_name).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

@app.post("/purchase")
def purchase_items(purchases: List[dict], db: Session = Depends(get_db)):
    for purchase in purchases:
        product_id = purchase.get('product_id')
        quantity = purchase.get('quantity')

        product = db.query(Product).filter(Product.name == product_id).first()
        if not product:
            raise HTTPException(status_code=404, detail=f"Product with id {product_id} not found")

        if product.stock_level < quantity:
            raise HTTPException(status_code=400, detail=f"Not enough stock for product {product.name}")

        product.stock_level -= quantity
        db.commit()

    return {"message": "Purchase successful"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
