from datetime import datetime
from datetime import timedelta
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends
from fastapi import HTTPException
from fastapi import status
from .settings import JWTSettings
from fastapi import Response
from jose import jwt, JWTError
import uuid
from models.models import User
from fastapi import Response



class JWTservice:
    def __init__(
        self,
        user: User,
        settings: JWTSettings
        ):
        
        self._user = user
        self._settings = settings

    
    def create_access_token(self):
        encoded_data = {"sub": self.user.id}
        expire_date = datetime.utcnow() + self._settings.access_token_expires
        encoded_data.update({"exp": expire_date})
        encoded_jwt = jwt.encode(
            encoded_data,
            self.settings.secret_key,
            algorithm=self.settings._algorithm)
        return encoded_jwt
    

