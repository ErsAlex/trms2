
from fastapi import APIRouter, Depends, status, Response
from common.auth.jwt import JWTservice
from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta
from api.user_api.dependencies import auth_service
from fastapi.exceptions import HTTPException
from common.auth.jwt import JWTservice
from common.auth.settings import JWTSettings as settings

router = APIRouter(
    prefix="/login",
    tags=["Login"],
)

@router.post("")
async def get_access_token(
        response: Response,
        database: auth_service,
        form_data: OAuth2PasswordRequestForm = Depends()):
    
    async with database.transaction() as session:
       current_user =  database.authenticate_user(
            session,
            form_data,
        )
       if not current_user:
           raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    access_token = JWTservice(current_user, settings.access_token_expires).create_access_token 
    response.set_cookie(key="access_token", value=f"Bearer {access_token}", httponly=True)
    