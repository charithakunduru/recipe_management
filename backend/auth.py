from passlib.context import CryptContext
from jose import jwt,JWTError
from fastapi.security import OAuth2PasswordBearer
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from fastapi import APIRouter,Depends,HTTPException
from database import get_db
from models import User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)
SECRET_KEY = "your_super_secret_key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# takes argument as login pwd
def hash_password(password: str):
    return pwd_context.hash(password)
def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)
def create_access_token(data: dict):
    to_encode = data.copy()

    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(
        to_encode,
        SECRET_KEY,
        algorithm=ALGORITHM
    )
    

    return encoded_jwt

def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials"
    )
    print("TOKEN RECEIVED:", token)
    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )
        print("PAYLOAD:", payload)
    except JWTError:
        raise credentials_exception

    email = payload.get("sub")
    print("EMAIL:", email)
    if email is None:
        raise credentials_exception

    user = db.query(User).filter(User.email == email).first()

    if user is None:
        raise credentials_exception

    return user