from typing import Annotated
from services.users.user_service import UserDatabaseService, get_service
from fastapi import Depends


service = Annotated[UserDatabaseService, Depends(get_service)]
