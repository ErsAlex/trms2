from sqlalchemy.ext.asyncio import AsyncSession
from common.database.base_service import BaseDataBaseService
from common.utils.hashing import get_password_hash
from models.models import User
from .settings import UserDatabaseSettings

class UserDatabaseService(BaseDataBaseService):

        async def create_user(
        self,
        session: AsyncSession,
        user_name: str, 
        user_surname: str,
        password: str,
        email: str
        ):
            new_user = User(
            user_name = user_name,
            user_surname = user_surname,
            email = email,
            password = get_password_hash(password)
        )
            await session.add(new_user)
            await session.commit()
            return new_user
     
def get_service():
    return UserDatabaseService(dsn=UserDatabaseSettings.db_dsn)