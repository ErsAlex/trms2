from fastapi import APIRouter, HTTPException
from api.room_api.rooms.schemas import RoomCreateSchema, RoomResponseSchema, RoomUpdateSchema, UpdateRoleSchema
from .dependencies import current_user_id, room_service, user_room_admin
from sqlalchemy.exc import IntegrityError
from fastapi import Depends
import uuid

router = APIRouter(prefix="/rooms", tags=["Rooms"])

@router.post("")
async def create_room(
    database: room_service,
    owner_id: current_user_id,
    room_data: RoomCreateSchema
    ):
    try:
        async with database.session.begin():
            responce = await database.create_room(
                session=database.session,
                name=room_data.name,
                description=room_data.description,
                owner_id=uuid.UUID(owner_id),
                )
            return responce
    except IntegrityError as err:
        raise HTTPException(status_code=503, detail=f"Database error: {err}")
    
@router.patch("/{room_id}/update")
async def update_room(
    room_data: RoomUpdateSchema,
    database: room_service,
    user_id: current_user_id,
    room: int = Depends(user_room_admin)
):
    try:
        data = room_data.model_dump()
        async with database.session.begin():
            updated_room = await database.update_room(
                session=database.session,
                room_id=room,
                data=data
            )
            return RoomResponseSchema.model_validate(updated_room)
    except IntegrityError as err:
        raise HTTPException(status_code=503, detail=f"Database error: {err}")

    