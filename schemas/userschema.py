from pydantic import BaseModel,EmailStr,Field
from typing import Optional

class UserCreate(BaseModel):
    username:str
    email:EmailStr
    password:str


class LoginRequest(BaseModel):
    email: str
    password: str





class UserResponse(BaseModel):
    id:int
    username:str
    email:str
    resume: Optional[str] = Field(None, description="Resume URL or details")

    class Config:
        form_attributes= True




