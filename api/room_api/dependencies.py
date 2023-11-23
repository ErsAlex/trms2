from typing import Annotated
from fastapi import Depends
from common.auth.rest import get_user_id_from_token
from services.rooms.room_service import RoomDatabaseService, get_room_service
from services.tasks.task_service import TaskDatabaseService, get_task_service
from fastapi import Request, Path
from services.rooms.settings import RoomDatabaseSettings
from services.rooms.access import RoomAccessValidator, AccessData



task_service = Annotated[TaskDatabaseService, Depends(get_task_service)]
room_service = Annotated[RoomDatabaseService, Depends(get_room_service)]
current_user_id = Annotated[str, Depends(get_user_id_from_token)]



async def admin_validate(
    database: room_service,
    user_id: current_user_id,
    room_id: int = Path(),
    ) -> AccessData:
    settings = RoomDatabaseSettings()
    roles = [settings.ROOM_ADMIN]
    room_access = RoomAccessValidator(database, roles)
    room_data: AccessData = await room_access.validate(database, user_id, room_id)
    return room_data


async def lead_validate(
    database: room_service,
    user_id: current_user_id,
    room_id: int = Path(),
    ) -> AccessData:
    settings = RoomDatabaseSettings()
    roles = [settings.ROOM_ADMIN, settings.ROME_LEAD]
    room_access = RoomAccessValidator(database, roles)
    room_data: AccessData = await room_access.validate(database, user_id, room_id)
    return room_data


async def common_access_validate(
    database: room_service,
    user_id: current_user_id,
    room_id: int = Path(),
    ) -> AccessData:
    settings = RoomDatabaseSettings()
    roles = [settings.ROOM_ADMIN, settings.ROME_LEAD, settings.ROOM_USER]
    room_access = RoomAccessValidator(database, roles)
    room_data: AccessData = await room_access.validate(database, user_id, room_id)
    return room_data
