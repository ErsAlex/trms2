
from common.database.base_service import BaseDataBaseService
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete, and_
from common.database.base_service import BaseDataBaseService
from models.models import Room, UserRoomAccess, RoomRole
import uuid
from .settings import RoomDatabaseSettings


class RoomDatabaseService(BaseDataBaseService):
    def __init__(self, settings: RoomDatabaseSettings):
        super().__init__(dsn=settings.db_dsn)
        self._settings = settings

    async def create_room(
        self,
        session: AsyncSession,
        name: str,
        description: str,
        owner_id: uuid.UUID
    ) -> Room:
        room = Room(
            name=name,
            description=description,
            owner_id=owner_id
            )
        room_accesses = UserRoomAccess(
            user_permissions=self._settings.ROOM_ADMIN,
            user_id=owner_id,
            room=room
            )
        session.add_all([room, room_accesses])
        return room
    
    async def update_room(
        self,
        session: AsyncSession,
        user_id: uuid.UUID,
        data: dict,
        ):
        stmt = update(Room).where(Room.id==user_id).values(**data).returning(Room)
        updated_room = await session.execute(stmt)
        updated_room = updated_room.scalar_one_or_none()
        return updated_room
    
    async def get_room_model(
        self,
        session: AsyncSession,
        room_id: int
    ):
        stmt = select(Room).where(Room.id==room_id)
        room = await session.execute(stmt)
        room = room.scalar_one_or_none()
        return room
    
    # placeholder, subject to be changed, need to add access delition
    async def delete_room(
        self,
        session: AsyncSession,
        room_id: int
    ):
        stmt_1 = delete(Room).where(id=room_id)
        await session.execute(stmt_1)
        return {"room_deleted_status": True}
    
    async def create_room_access(
        self,
        session: AsyncSession,
        user_id: uuid.UUID,
        room_id: int
    ):
        room_access = UserRoomAccess(
            user_id=user_id,
            room_id=room_id
        )
        session.add(room_access)
        return room_access

    async def access_room(
        self,
        session: AsyncSession,
        user_id: uuid.UUID,
        room_id: int
    ):
        query = select(Room).join(UserRoomAccess).where(and_(
            UserRoomAccess.user_id==user_id,
            UserRoomAccess.room_id==room_id
            ))
        room = await session.execute(query)
        return room.scalar_one_or_none()

    async def update_user_role(
        self,
        session: AsyncSession,
        room_id: int,
        user_id: uuid.UUID,
        data: dict
        ):
        stmt = update(UserRoomAccess).where(and_(
            UserRoomAccess.room_id==room_id,
            UserRoomAccess.user_id==user_id
            )).values(**data)
        await session.execute(stmt)
        return {"access_updated_status": True}
    
    
def get_room_service():
    return RoomDatabaseService(settings=RoomDatabaseSettings)