from typing import Annotated
from fastapi import Depends
from common.auth.rest import get_user_id_from_token, get_user_data_from_token
import uuid
from services.rooms.room_service import RoomDatabaseService, get_room_service
from services.tasks.task_service import TaskDatabaseService, get_task_service
from services.tasks.settings import TaskDatabaseSettings
from fastapi import Request, Path, HTTPException
from services.rooms.settings import RoomDatabaseSettings
from sqlalchemy.exc import IntegrityError

task_service = Annotated[TaskDatabaseService, Depends(get_task_service)]
room_service = Annotated[RoomDatabaseService, Depends(get_room_service)]
current_user_id = Annotated[str, Depends(get_user_id_from_token)]
current_user_data = Annotated[dict, Depends(get_user_data_from_token)]

async def user_in_room(
    database: room_service,
    user_id: current_user_id,
    room_id: int = Path(),
    ):
    try:
        id = uuid.UUID(user_id)
        async with database.session.begin():
            permissions= await database.get_user_role_in_room(
                database.session,
                room_id,
                id
            )
        if not permissions:
            raise HTTPException(status_code=403, message="access denied")
        return permissions
    except IntegrityError as err:
        raise HTTPException(status_code=503, detail=f"Database error: {err}")


async def user_room_admin_prms(
    database: room_service,
    user_id: current_user_id,
    room_id: int = Path(),
    ):  
    settings = RoomDatabaseSettings()
    try:
        id = uuid.UUID(user_id)
        async with database.session.begin():
            permissions= await database.get_user_role_in_room(
                database.session,
                room_id,
                id
            )
        if permissions != settings.ROOM_ADMIN:
            raise HTTPException(status_code=403, detail=f"User {user_id} is not an admin in room {room_id}")
        return room_id
    except IntegrityError as err:
        raise HTTPException(status_code=503, detail=f"Database error: {err}")


async def user_room_lead_prms(
    database: room_service,
    user_id: current_user_id,
    room_id: int = Path(),
    ):  
    settings = RoomDatabaseSettings()
    try:
        id = uuid.UUID(user_id)
        async with database.session.begin():
            permissions= await database.get_user_role_in_room(
                database.session,
                room_id,
                id
            )
        if permissions != settings.ROME_LEAD or permissions != settings.ROOM_ADMIN:
            raise HTTPException(status_code=403, detail=f"User {user_id} is not an lead or admin in room {room_id}")
        return room_id
    except IntegrityError as err:
        raise HTTPException(status_code=503, detail=f"Database error: {err}")

async def default_room_user(
    database: room_service,
    user_id: current_user_id,
    room_id: int = Path(),
    ):  
    settings = RoomDatabaseSettings()
    try:
        id = uuid.UUID(user_id)
        async with database.session.begin():
            permissions= await database.get_user_role_in_room(
                database.session,
                room_id,
                id
            )
        if permissions != settings.ROOM_USER:
            raise HTTPException(status_code=403, detail=f"User {user_id} is not  in room {room_id}")
        return room_id
    except IntegrityError as err:
        raise HTTPException(status_code=503, detail=f"Database error: {err}")
    
