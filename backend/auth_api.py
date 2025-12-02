from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from typing import Dict
from passlib.context import CryptContext
import jwt
import time
import json
import logging

SECRET_KEY = "your-secret-key"  # Change this in production
ALGORITHM = "HS256"

router = APIRouter()

# Use a relative path for users.json
USERS_FILE = "backend/users.json"

logger = logging.getLogger("backend_logger")

def load_users():
    try:
        with open(USERS_FILE, "r") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}

def save_users():
    import os
    dir_path = os.path.dirname(USERS_FILE)
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)
    with open(USERS_FILE, "w") as f:
        json.dump(users_db, f)

# In-memory user store
users_db: Dict[str, Dict] = load_users()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/login")

class UserRegister(BaseModel):
    username: str
    password: str

@router.post("/api/register")
def register(user: UserRegister):
    # Always truncate password to 72 characters before any operation
    password = user.password[:72]
    logger.info("Register endpoint called with username=%s", user.username)
    if user.username in users_db:
        logger.warning("Registration failed: username '%s' already exists", user.username)
        raise HTTPException(status_code=400, detail="Username already registered")
    hashed_password = pwd_context.hash(password)
    users_db[user.username] = {"username": user.username, "password": hashed_password}
    save_users()
    logger.info("User '%s' registered successfully", user.username)
    return {"msg": "User registered successfully"}

@router.post("/api/login")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    logger.info("Login endpoint called with username=%s", form_data.username)
    user = users_db.get(form_data.username)
    if not user or not pwd_context.verify(form_data.password, user["password"]):
        logger.warning("Login failed for username=%s", form_data.username)
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token_data = {"sub": user["username"], "exp": int(time.time()) + 3600}
    token = jwt.encode(token_data, SECRET_KEY, algorithm=ALGORITHM)
    logger.info("User '%s' logged in successfully", form_data.username)
    return {"access_token": token, "token_type": "bearer"}

# Dependency to get current user

def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if username is None or username not in users_db:
            logger.warning("Token authentication failed: invalid username")
            raise HTTPException(status_code=401, detail="Invalid authentication")
        logger.info("Token authentication succeeded for username=%s", username)
        return users_db[username]
    except jwt.PyJWTError:
        logger.warning("Token authentication failed: JWT error")
        raise HTTPException(status_code=401, detail="Invalid authentication")

@router.get("/api/me")
def read_users_me(current_user: dict = Depends(get_current_user)):
    logger.info("/api/me endpoint called for username=%s", current_user["username"])
    return {"username": current_user["username"]}
