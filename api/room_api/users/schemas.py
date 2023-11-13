from pydantic import  BaseModel, ConfigDict
from models.models import RoomRole
import uuid

class CreateAccessSchema(BaseModel):
    user_id: uuid.UUID


class AccessResponse(BaseModel):

    model_config = ConfigDict(from_attributes=True)
    id: int
    user_permissions: RoomRole
    user_id: uuid.UUID
    room_id: int
    
class AccessUpdateSchema(BaseModel):
    user_id: uuid.UUID
    new_role: str
    
    