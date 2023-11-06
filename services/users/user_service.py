from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete
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
        
        async def update_user(
            self,
            session: AsyncSession,
            filter_by,
            data: dict,
        ):
            stmt = update(User).values(**data).filter_by(**filter_by).returning(User)
            updated_user = await session.execute(stmt)
            updated_user = updated_user.scalar_one_or_none()
            return updated_user
        
        async def get_user(
            self,
            session: AsyncSession,
            filter_by
        ):            
            stmt = select(User).filter_by(**filter_by)
            user = await session.execute(stmt)
            user = user.scalar_one_or_none()
            return user
        
        async def delete_user(
            self,
            session: AsyncSession,
            filter_by
        ):
            stmt = delete(User).filter_by(**filter_by)
            await session.execute(stmt)
            return {"user_deleted": True}
        
        
def get_user_service():
    return UserDatabaseService(dsn=UserDatabaseSettings.db_dsn)