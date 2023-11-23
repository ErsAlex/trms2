from fastapi import APIRouter, Depends
from api.room_api.dependencies import room_service, lead_validate, common_access_validate, admin_validate
from .schemas import AccessUpdateSchema
import uuid
from services.rooms.access import AccessData




router = APIRouter(prefix="/rooms", tags=["Room_User"])


@router.post('/{room_id}/invite')
async def invite_user(
    database: room_service,
    new_user_id: uuid.UUID,
    access_data: AccessData = Depends(lead_validate)
):
    async with database.session.begin():
        response =  await database.create_access_for_user(
            session=database.session,
            room_id=access_data.room_id,
            user_id=new_user_id
        )
        return response

@router.delete('/{room_id}/kick')
async def kick_user(
    database: room_service,
    kick_user_id: uuid.UUID,
    access_data: AccessData = Depends(lead_validate)
):
    async with database.session.begin():
        response =  await database.delete_access_for_user(
            session=database.session,
            room_id=access_data.room_id,
            user_id=kick_user_id
        )
        return response
    
    
@router.patch("/{room_id}/promote")
async def update_user_role(
    database: room_service,
    data: AccessUpdateSchema,
    access_data: AccessData = Depends(admin_validate)
        
):
    data = data.model_dump()
    async with database.session.begin():
        response =  await database.update_user_role(
        session=database.session,
        room_id=access_data.room_id,
        data=data
        )
        return response