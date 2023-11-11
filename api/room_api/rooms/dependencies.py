from typing import Annotated
from fastapi import Depends
from common.auth.rest import get_user_id_from_token
import uuid
from services.rooms.room_service import RoomDatabaseService, get_room_service
from fastapi import Request, Path, HTTPException
from services.rooms.settings import RoomDatabaseSettings
from sqlalchemy.exc import IntegrityError


room_service = Annotated[RoomDatabaseService, Depends(get_room_service)]
current_user_id = Annotated[str, Depends(get_user_id_from_token)]


async def user_room_admin(
    database: room_service,
    # may not work
    room_id: int = Path(),
    user_id: str = Depends(get_user_id_from_token)
    ) -> int:
    try:
        async with database.session.begin():
            id = uuid(user_id)
            permissions= await database.get_user_role_in_room(
                database.session,
                room_id,
                id
            )
            if permissions != RoomDatabaseSettings.ROOM_ADMIN:
                raise HTTPException(status_code=403, detail=f"User {user_id} is not an admin in room {room_id}")
    except IntegrityError as err:
        raise HTTPException(status_code=503, detail=f"Database error: {err}")
    return room_id