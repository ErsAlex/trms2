
from common.database.base_service import BaseDataBaseService
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete, and_
from common.database.base_service import BaseDataBaseService
from models.models import Room, UserRoomAccess, RoomRole, Task, TaskAssignment, TaskHistory, User
import uuid
from .settings import TaskDatabaseSettings
from common.tasks.system_messages import SystemMessage

class TaskDatabaseService(BaseDataBaseService):
    def __init__(self, settings: TaskDatabaseSettings,
        default_messages: SystemMessage
        ):
        super().__init__(dsn=settings.db_dsn)
        self._settings = settings
        self.default_messages = default_messages
        
    async def create_task(
        self,
        session: AsyncSession,
        room_id: int,
        user_id: uuid.UUID,
        task_name: str,
        task_description: str
        ):
        task = Task(
            task_name=task_name,
            description=task_description,
            owner_id=user_id,
            room_id=room_id
            )
        task_history = TaskHistory(
            message=self.default_messages.task_created_message,
            author_id=user_id,
            task=task             
        )
        session.add_all[task, task_history]
        await session.commit()
        return {"task_created": True}
    
    
    async def get_user_in_room(
        self,
        session: AsyncSession,
        user_id: uuid.UUID,
        room_id: int
        ):
        query = select(User, Room).join(UserRoomAccess).where(and_(UserRoomAccess.user_id == user_id, UserRoomAccess.room_id==room_id))
        result = await session.execute(query)
        result = result.scalar_one_or_none()
        return result
    
def get_task_service():
    return TaskDatabaseService(
        settings=TaskDatabaseSettings(),
        default_messages=SystemMessage()
        )

