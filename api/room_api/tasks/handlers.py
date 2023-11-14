from fastapi import APIRouter, HTTPException
from api.room_api.tasks.schemas import TaskCreateSchema
from api.room_api.dependencies import current_user_id, room_service, user_room_admin_prms, user_room_lead_prms
from sqlalchemy.exc import IntegrityError
from fastapi import Depends
import uuid

router = APIRouter(prefix="/rooms", tags=["Tasks"])


