import uuid
import enum
from sqlalchemy import text, types, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, declarative_base, relationship
from typing import Annotated, List

from datetime import datetime

Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id: Mapped[uuid.UUID] = mapped_column(types.UUID, primary_key=True, default=uuid.uuid4)
    user_name: Mapped[str] = mapped_column(nullable=False)
    user_surname: Mapped[str] = mapped_column(nullable=False)
    email: Mapped[str] = mapped_column(unique=True, nullable=False)
    is_active: Mapped[bool] = mapped_column(default=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    created_at: Mapped[datetime] = mapped_column(default=datetime.now)
    updated_at: Mapped[datetime] = mapped_column(default=datetime.now, onupdate=datetime.now)
    created_rooms: Mapped[List["Room"]] = relationship(back_populates="owner")
    room_accesses: Mapped[List['UserRoomAccess']] = relationship(back_populates="user")
    created_tasks: Mapped[List["Task"]] = relationship(back_populates="owner")
    assigned_tasks: Mapped[List["TaskAssignment"]] = relationship(back_populates="user")
    

class Room(Base):
    __tablename__ = "rooms"
    id: Mapped[int] = mapped_column(primary_key=True)
    owner_id: Mapped[uuid.UUID] = mapped_column(types.UUID, ForeignKey("users.id"))
    name: Mapped[str] = mapped_column(nullable=False)
    description: Mapped[str] = mapped_column(nullable=True)
    is_active: Mapped[bool] = mapped_column(nullable=False, default=True)
    owner: Mapped["User"] = relationship(back_populates="created_rooms")
    created_at: Mapped[datetime] = mapped_column(default=datetime.now)
    owner: Mapped["User"] = relationship(back_populates="created_rooms")
    room_accesses: Mapped[List["UserRoomAccess"]] = relationship(back_populates="room")
    tasks: Mapped[List["Task"]] = relationship(back_populates="room")

class RoomRole(str, enum.Enum):

    ROOM_ADMIN = "ROOM_ADMIN"

    ROME_LEAD = "ROME_LEAD"

    ROOM_USER = "ROOM_USER"


class UserRoomAccess(Base):
    __tablename__ = "room_access"
    id: Mapped[int] = mapped_column(primary_key=True)
    user_permissions: Mapped[RoomRole] = mapped_column(default=RoomRole.ROOM_USER)
    user_id: Mapped[uuid.UUID] = mapped_column(types.UUID, ForeignKey("users.id"))
    room_id: Mapped[int] = mapped_column(ForeignKey("rooms.id"))
    user: Mapped["User"] = relationship(back_populates="room_accesses")
    room: Mapped["Room"] = relationship(back_populates="room_accesses")
    
    
class Task(Base):
    __tablename__ = "tasks"

    id: Mapped[int] = mapped_column(primary_key=True)
    owner_id: Mapped[uuid.UUID] = mapped_column(types.UUID, ForeignKey("users.id"))
    task_name: Mapped[str] = mapped_column(nullable=False)
    room_id: Mapped[int] = mapped_column(ForeignKey("rooms.id"))
    created_at: Mapped[datetime] = mapped_column(default=datetime.now)
    updated_at: Mapped[datetime] = mapped_column(default=datetime.now, onupdate=datetime.now)
    description: Mapped[str] = mapped_column(nullable=True)
    is_assigned: Mapped[bool] = mapped_column(default=False)
    is_active: Mapped[bool] = mapped_column(default=True)
    owner: Mapped["User"] = relationship(back_populates="created_tasks")
    room: Mapped["Room"] = relationship(back_populates="tasks")
    assignments: Mapped[List["TaskAssignment"]] = relationship(back_populates="task")
    task_history: Mapped[List["TaskHistory"]] = relationship(back_populates="task")


class TaskHistory(Base):
    __tablename__ = "task_history"
    id: Mapped[int] = mapped_column(primary_key=True)
    task_id: Mapped[int] = mapped_column(ForeignKey("tasks.id"))
    message: Mapped[str] = mapped_column(nullable=True)
    author_id: Mapped[uuid.UUID] = mapped_column(types.UUID, nullable=True)
    created_at: Mapped[datetime] = mapped_column(default=datetime.now)
    updated_at: Mapped[datetime] = mapped_column(default=datetime.now, onupdate=datetime.now)
    task: Mapped["Task"] = relationship(back_populates="task_history")
    
class TaskAssignment(Base):
    __tablename__ = "task_assignments"
    id: Mapped[int] = mapped_column(primary_key=True)
    created_at: Mapped[datetime] = mapped_column(default=datetime.now)
    task_id: Mapped[int] = mapped_column(ForeignKey("tasks.id"))
    user_id: Mapped[uuid.UUID] = mapped_column(types.UUID, ForeignKey("users.id"))
    task: Mapped["Task"] = relationship(back_populates='assignments')
    user: Mapped["User"] = relationship(back_populates="assigned_tasks")