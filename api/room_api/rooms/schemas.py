

from pydantic import BaseModel, ConfigDict
import uuid
import datetime
from models.models  import RoomRole

class RoomCreateSchema(BaseModel):
    name: str
    description: str


class RoomUpdateSchema(BaseModel):
    name: str
    description: str


class RoomResponseSchema(BaseModel):

    model_config = ConfigDict(from_attributes=True)

    id: int
    owner_id: uuid.UUID
    created_at: datetime.datetime
    updated_at: datetime.datetime
    name: str
    description: str
    is_active: bool



class UpdateRoleSchema(BaseModel):
    user_id: uuid.UUID
    user_permissions: RoomRole


class UpdatedRoleResponseSchema(BaseModel):
    user_id: uuid.UUID
    new_role: str


class AccessSchema(BaseModel):
    user_id: uuid.UUID


class AccessResponse(BaseModel):

    model_config = ConfigDict(from_attributes=True)
    id: int
    user_permissions: RoomRole
    user_id: uuid.UUID
    room_id: int



class AccessUpdateResponse(BaseModel):

    user_id: uuid.UUID
    room_id: int
    access_granted: bool = False
    access_revoked: bool = False
    role_updated: bool = False
    user_role: RoomRole