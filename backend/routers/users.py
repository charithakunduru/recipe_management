from fastapi import APIRouter,Depends,HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from database import SessionLocal
from database import get_db
from models import User
from schemas import UserCreate,UserLogin
from passlib.context import CryptContext
from auth import hash_password, verify_password,create_access_token,get_current_user

router = APIRouter()

@router.post("/register")
def register(user: UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.email == user.email).first()
    if existing_user:
        return {"error": "Email already registered"}
    # pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    hashed_password = hash_password(user.password)
    new_user = User(
    username=user.username,
    email=user.email,
    hashed_password=hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"message": "User registered successfully", "user_id": new_user.id}
#login api creation
@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.email == form_data.username).first()
    if not db_user:
        raise HTTPException(status_code=400, detail="Invalid email or password")
    if not verify_password(form_data.password, db_user.hashed_password):
        raise HTTPException(status_code=400, detail="Invalid email or password")
    access_token = create_access_token(data={"sub": db_user.email})
    return {"access_token": access_token, "token_type": "bearer"}       
