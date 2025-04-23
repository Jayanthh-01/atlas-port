from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from services.authentication import (
    create_access_token,
    verify_password,
    hash_password
)
from pydantic import EmailStr
from services.user_service import get_user_by_email, create_user
from config.db import get_db
from schemas.userschema import LoginRequest, UserCreate

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import timedelta
from typing import Dict, Any

auth_router = APIRouter(tags=["Authentication"])

@auth_router.post("/login", response_model=Dict[str, str])
async def login(data: LoginRequest, db: Session = Depends(get_db)):
    user = get_user_by_email(db, data.email)  
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Bearer"}
        )
    
    if not verify_password(data.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Bearer"}
        )
    
    access_token = create_access_token(
        data={"sub": str(user.id)} 
    )
    return {"access_token": access_token, "token_type": "bearer" ,"username":user.username}

@auth_router.post("/register", status_code=status.HTTP_201_CREATED)
async def register(data: UserCreate, db: Session = Depends(get_db)):
    # Check if user exists
    if get_user_by_email(db, data.email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    try:
        # Hash password and create user in one step
        hashed_password = hash_password(data.password)
        user_data = data.dict(exclude={"password"})
        user_data.update({"password": hashed_password})
        
        new_user = create_user(db=db, user=UserCreate(**user_data))
        
        if not new_user:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="User registration failed"
            )
            
        return {
            "message": "User registered successfully",
            "user": {
                "id": new_user.id,
                "username": new_user.username,
                "email": new_user.email
            }
        }
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Registration error: {str(e)}"
        )