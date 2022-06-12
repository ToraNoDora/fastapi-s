from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from src.store.db import get_store
from src.store.hashing_password import verify_password
from src.store.models.users import User
from src.core.jwt import create_access_token


router = APIRouter()


@router.post("/login")
def login(request: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_store)):
    """User authorization"""
    user = db.query(User).filter(User.email == request.username).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Invalid credentials..",
        )

    if not verify_password(request.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid password..",
        )

    access_token = create_access_token(data={"sub": user.email})

    auth_data = {
        "access_token": access_token,
        "token_type": "bearer",
        }

    return auth_data


