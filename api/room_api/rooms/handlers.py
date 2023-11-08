from fastapi import APIRouter, HTTPException
from api.room_api.rooms.schemas import RoomCreateSchema, RoomResponseSchema, RoomUpdateSchema, UpdateRoleSchema, UpdatedRoleResponse
from .dependencies import current_user_id, room_service, user_room_admin
from sqlalchemy.exc import IntegrityError

router = APIRouter(prefix="/rooms", tags=["Rooms"])

@router.post("")
async def create_room(
    database: room_service,
    owner_id: current_user_id,
    room_data: RoomCreateSchema
    ):
    try:
        async with database.transaction() as session:
            room = await database.create_room(
                session,
                room_data.name,
                room_data.description,
                owner_id
                )
            return RoomResponseSchema.model_validate(room)
    except IntegrityError as err:
        raise HTTPException(status_code=503, detail=f"Database error: {err}")
    
@router.patch("/{room_id}/update")
async def update_room(
    room_data: RoomUpdateSchema,
    database: room_service,
    user_id: current_user_id,
    room_id: user_room_admin
):
    try:
        data = room_data.model_dump()
        async with database.transaction() as session:
            updated_room = await database.update_room(
                session,
                user_id,
                room_id,
                data
            )
            return RoomResponseSchema.model_validate(updated_room)
    except IntegrityError as err:
        raise HTTPException(status_code=503, detail=f"Database error: {err}")

    