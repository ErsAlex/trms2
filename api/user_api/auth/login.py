
from fastapi import APIRouter, Depends, status, Response
from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta
from api.user_api.dependencies import auth_service
from fastapi.exceptions import HTTPException
from common.auth.jwt import create_token
from common.auth.settings import JWTSettings
from api.user_api.schemas import UserSchema

router = APIRouter(
    prefix="/login",
    tags=["Login"],
)

@router.post("")
async def get_access_token(
        response: Response,
        database: auth_service,
        form_data: OAuth2PasswordRequestForm = Depends()):
    
    async with database.session.begin():
       current_user = await database.authenticate_user(
            database.session,
            form_data
            )
    if current_user:
        access_token_expired = timedelta(minutes=30)
        refresh_token_expired = timedelta(minutes=35)
        user_id = str(current_user.id)
        access_token = create_token(data={"sub": user_id},
                                expiration_delta=access_token_expired)
        refresh_token = create_token(data={"sub": user_id}, expiration_delta=refresh_token_expired)
        response.set_cookie(key="access_token", value=f"Bearer {access_token}", httponly=True)
        return {"status": "token issued", "access_token": access_token, "refresh_token": refresh_token}

    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
        
    