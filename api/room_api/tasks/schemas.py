import datetime
from models.models import RoomRole
from pydantic import BaseModel, ConfigDict
import uuid



class TaskCreateSchema(BaseModel):
    task_name: str
    description: str


class TaskResponseSchema(BaseModel):

    model_config = ConfigDict(from_attributes=True)

    id: int
    task_name: str
    description: str
    date_created: datetime.datetime
    date_updated: datetime.datetime
    owner_id: uuid.UUID
    room_id: int
    is_assigned: bool
    is_active: bool
