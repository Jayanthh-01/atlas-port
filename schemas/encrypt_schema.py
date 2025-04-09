from  pydantic_setting import BaseSettings
from dotenv import load_dotenv

load_dotenv()
class Settings(BaseSettings):
    secret_key: str =os.getenv("SECRET_KEY")
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30

    class Config:
        env_file = ".env"
        extra = "allow" 
