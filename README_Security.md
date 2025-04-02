
# 🛡️ OWASP Top 10 Security Implementation - FastAPI Project Report

This document explains how each relevant OWASP Top 10 risk is mitigated in the FastAPI project using practical code examples and explanations.

---

## 1. Broken Access Control

**What it means**: Prevent users from accessing or modifying data they don't own (e.g., reordering someone else's order).

**Example attack**: User tries to POST `/orders/123/reorder`, where order 123 belongs to another user.

**How we implement it (IDOR protection)**:
```python
@router.post("/orders/{order_id}/reorder")
def reorder(order_id: int, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    if order.customer_name != current_user.username:
        raise HTTPException(status_code=403, detail="Access denied")

    if order.status != "completed":
        raise HTTPException(status_code=400, detail="Only completed orders can be reordered.")

    new_order = Order(
        customer_name=order.customer_name,
        status="pending",
        total_price=order.total_price
    )
    db.add(new_order)
    db.commit()
    db.refresh(new_order)
    return {"message": "Reorder created", "new_order_id": new_order.id}
```

✅ This prevents users from accessing orders they don't own.

**Additional protections**:
```python
@app.get("/orders/me")
def get_my_orders(current_user = Depends(get_current_user)):
    return fetch_orders_for_user(current_user.username)
```

✅ Ensures that all protected endpoints enforce authentication.

```python
def require_admin(user = Depends(get_current_user)):
    if user.role_id != 1:
        raise HTTPException(status_code=403, detail="Admins only")
    return user

@app.get("/photos/all")
def get_all_photos(current_user = Depends(require_admin)):
    ...
```

✅ Only admins can access certain endpoints, enforcing role-based access control (RBAC).

---

## 2. Cryptographic Failures

**What it means**: Passwords, tokens, or secrets must be protected using strong cryptography.

**Example attack**: Storing passwords in plain text, or leaking secrets in logs.

**How we implement it**:
- Passwords are hashed using `bcrypt` via `passlib`:
```python
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
```

- Tokens use a securely loaded secret key:
```python
from dotenv import load_dotenv
load_dotenv()
SECRET_KEY = os.getenv("JWT_SECRET_KEY")
```

✅ No plain-text passwords, and secrets are kept in `.env`.

---

## 3. Injection

**What it means**: Protect the server from SQL/command injection and file upload abuse.

**Example attack**: Uploading a `.php` file disguised as an image, or SQL via input.

**How we implement it**:
- SQLAlchemy ORM prevents raw query injection:
```python
order = db.query(Order).filter(Order.id == order_id).first()
```

✅ No raw SQL queries used in endpoints.

- Uploaded files are validated and sanitized:
```python
def validate_image(file: UploadFile):
    ext = os.path.splitext(file.filename)[1].lower()
    if ext not in ['.jpg', '.jpeg', '.png']:
        raise HTTPException(status_code=400, detail="Invalid file format.")
    file.file.seek(0, 2)
    size = file.file.tell()
    if size > 5 * 1024 * 1024:
        raise HTTPException(status_code=400, detail="File too large")
    file.file.seek(0)
```

✅ Ensures only safe image formats and size are accepted.

- Rejecting dangerous content types:
```python
import magic

def validate_content_type(file: UploadFile):
    mime = magic.from_buffer(file.file.read(2048), mime=True)
    file.file.seek(0)
    if not mime.startswith("image/"):
        raise HTTPException(status_code=400, detail="Unsupported content type")
```

✅ Blocks potentially dangerous content types (e.g., HTML, JS).

---

## 5. Security Misconfiguration

**What it means**: Default or insecure settings can expose your app (e.g., debug=True, stack traces in prod).

**How we implement it**:
- `debug=False` in production:
```python
app = FastAPI(debug=False)
```

✅ Prevents accidental exposure of stack traces.

- Custom global error handler:
```python
@app.exception_handler(Exception)
async def generic_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error."}
    )
```

✅ Hides internal exceptions from users while optionally logging them internally.

---

## 6. Vulnerable and Outdated Components

**What it means**: Using outdated libraries can introduce known vulnerabilities.

**How we implement it**:
- We use **Snyk** to scan and monitor dependencies.
```bash
snyk test
snyk monitor
```

✅ Snyk alerts us to unsafe packages and suggests upgrades.

---

## 7. Identification and Authentication Failures

**What it means**: Protect login endpoints and enforce secure authentication.

**Example attack**: Brute-forcing the `/token` endpoint.

**How we implement it**:
- Use JWT tokens via `OAuth2PasswordBearer`
- Rate limit login with SlowAPI:
```python
@limiter.limit("5/minute")
@app.post("/token")
def login(...): ...
```

✅ Prevents abuse and ensures secure login with tokens.

---

## 2. Cryptographic Failures

**What it means**: Passwords, tokens, or secrets must be protected using strong cryptography.

**Example attack**: Storing passwords in plain text, or leaking secrets in logs.

**How we implement it**:
- Passwords are hashed using `bcrypt` via `passlib`:
```python
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
```

---

## 6. Vulnerable and Outdated Components

**What it means**: Using outdated libraries can introduce known vulnerabilities.

**How we implement it**:
- We use **Snyk** to scan and monitor dependencies.
```bash
snyk test
snyk monitor
```

✅ Snyk alerts us to unsafe packages and suggests upgrades.

---

## 7. Identification and Authentication Failures

**What it means**: Protect login endpoints and enforce secure authentication.

**Example attack**: Brute-forcing the `/token` endpoint.

**How we implement it**:
- Use JWT tokens via `OAuth2PasswordBearer`
- Rate limit login with SlowAPI:
```python
@limiter.limit("5/minute")
@app.post("/token")
def login(...): ...
```

✅ Prevents abuse and ensures secure login with tokens.

---
