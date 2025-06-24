from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from ..schemas.user import UserCreate
from .. import models, database
from ..core.security import hash_password, pwd_context
from fastapi.security import OAuth2PasswordRequestForm
from ..core import token

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/register")
def register(user: UserCreate, db: Session = Depends(database.get_db)):
    existing_user = db.query(models.User).filter(models.User.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    hashed_pw = hash_password(user.password)

    new_user = models.User(
        username = user.username,
        email = user.email,
        hashed_password = hashed_pw
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {"msg": "User registered succesfully", "user_id": new_user.id}

@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):
    user = db.query(models.User).filter(models.User.username == form_data.username).first()
    
    if not user or not pwd_context.verify(form_data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid email or password")
    
    access_token = token.create_access_token(data={"sub": user.email})
    
    return {"access_token": access_token, "token_type": "bearer"}