from schemas.userschema import UserCreate
from sqlalchemy.orm import Session
from models.user_model import User


def create_user(db:Session,user:UserCreate):
    new_user=User(
        username=user.username,
        email=user.email,
        password=user.password

    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

def get_user(db:Session,user_id:int):
    user=db.query(User).filter(User.id==user_id).first()
    return user

def get_user_by_email(db:Session,email:str):
    return db.query(User).filter(User.email==email).first()