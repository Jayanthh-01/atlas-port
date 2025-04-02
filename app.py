from fastapi import FastAPI
from routes.user_route import router as user_router
from routes.auth_route import auth_router
from config.db import Base,engine

app=FastAPI()

Base.metadata.create_all(bind=engine)

@app.get("/")
def index():
    return {" hello world"}


app.include_router(user_router,prefix="/users",tags=["Users"])

app.include_router(auth_router,prefix="/auth",tags=["Auth"])