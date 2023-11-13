from fastapi import APIRouter, Depends
from api.room_api.dependencies import room_service, user_room_lead_prms, user_room_admin_prms
from .schemas import AccessUpdateSchema
import uuid
router = APIRouter(prefix="/rooms", tags=["Room_User"])


@router.post('/{room_id}/invite')
async def invite_user(
    database: room_service,
    new_user_id: uuid.UUID,
    room_id: int = Depends(user_room_lead_prms)
):
    async with database.session.begin():
        response =  await database.create_access_for_user(
            session=database.session,
            room_id=room_id,
            user_id=new_user_id
        )
        return response

@router.delete('/{room_id}/kick')
async def kick_user(
    database: room_service,
    kick_user_id: uuid.UUID,
    room_id: int = Depends(user_room_admin_prms)
):
    async with database.session.begin():
        response =  await database.delete_access_for_user(
            session=database.session,
            room_id=room_id,
            user_id=kick_user_id
        )
        return response
    
    
@router.patch("/{room_id}/promote")
async def update_user_role(
    database: room_service,
    data: AccessUpdateSchema,
    room_id: int = Depends(user_room_admin_prms)
        
):
    data = data.model_dump()
    async with database.session.begin():
        response =  await database.update_user_role(
        session=database.session,
        room_id=room_id,
        data=data
        )
        return response