from pydantic_settings import BaseSettings
from datetime import timedelta

class JWTSettings(BaseSettings):
    
    access_token_expires: timedelta = timedelta(minutes=30)
    refresh_token_expires: timedelta  = timedelta(minutes=35)
    
    secret_key: str = "secret_key"
    
    algorithm: str = "HS256"