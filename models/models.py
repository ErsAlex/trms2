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
