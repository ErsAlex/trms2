from typing import Annotated
from services.users.user_service import UserDatabaseService, get_user_service
from fastapi import Depends
from services.users.auth_service import AuthService, get_auth_service

user_service = Annotated[UserDatabaseService, Depends(get_user_service)]

auth_service = Annotated[AuthService,  Depends(get_auth_service)]