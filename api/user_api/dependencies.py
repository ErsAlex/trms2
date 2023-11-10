from typing import Annotated
from services.users.user_service import UserDatabaseService, get_user_service
from fastapi import Depends
from services.users.auth_service import AuthService, get_auth_service
from common.auth.rest import get_user_id_from_token
import uuid
from models.models  import User

user_service = Annotated[UserDatabaseService, Depends(get_user_service)]

auth_service = Annotated[AuthService,  Depends(get_auth_service)]


async def get_current_user(
    database: UserDatabaseService = Depends(get_user_service),
    user_id: uuid.UUID = Depends(get_user_id_from_token)) -> User:
    async with database.session.begin():
        user = await database.get_user(
            database.session,
            id=user_id
        )
        return user