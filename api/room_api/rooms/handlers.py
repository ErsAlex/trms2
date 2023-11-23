from fastapi import APIRouter, HTTPException
from api.room_api.rooms.schemas import RoomCreateSchema, RoomResponseSchema, RoomUpdateSchema, UpdateRoleSchema
from api.room_api.dependencies import current_user_id, room_service, admin_validate
from sqlalchemy.exc import IntegrityError
from fastapi import Depends
import uuid
from services.rooms.access import AccessData


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
    access_data: AccessData = Depends(admin_validate)
):
    try:
        data = room_data.model_dump()
        async with database.session.begin():
            updated_room = await database.update_room(
                session=database.session,
                room_id=access_data.room_id,
                data=data
            )
            return RoomResponseSchema.model_validate(updated_room)
    except IntegrityError as err:
        raise HTTPException(status_code=503, detail=f"Database error: {err}")

    