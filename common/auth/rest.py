
from fastapi import Depends
from fastapi import HTTPException
from fastapi import status
from .settings import JWTSettings
from jose import jwt, JWTError
import uuid
from .utils import OAuth2PasswordBearerWithCookie

oauth2_scheme = OAuth2PasswordBearerWithCookie(tokenUrl="/login")

async def get_user_id_from_token(token: str = Depends(oauth2_scheme)):
    exeption = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="invalid credentials")
    try:
        payload = jwt.decode(
            token,
            JWTSettings.secret_key,
            algorithms=[JWTSettings.algorithm]
            )
        data: str = payload.get('sub')
        if data is None:
            raise exeption
    except JWTError:
        raise exeption
    user_id = uuid.UUID(data)
    return user_id

