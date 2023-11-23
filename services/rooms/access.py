from . room_service import RoomDatabaseService
import uuid
from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from dataclasses import dataclass

@dataclass
class AccessData:
    user_id: uuid.UUID
    room_id: int


class RoomAccessValidator:
    def __init__(self, database: RoomDatabaseService, role_name: list):
        self.role_name = role_name
        self.database = database
        
        
    async def validate(self, user_id: uuid.UUID, room_id: int):
        async with self.database.session.begin():
            try:
                permissions = await self.database.get_user_role_in_room(
                    session=self.database.session,
                    user_id=user_id,
                    room_id=room_id,
                )
                if permissions not in self.role_name:
                    raise HTTPException(status_code=403, message="access denied")
                access_data = AccessData(user_id, room_id)
                return access_data
            except IntegrityError as err:
                raise HTTPException(status_code=503, detail=f"Database error: {err}")