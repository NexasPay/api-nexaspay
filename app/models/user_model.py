from typing import List, TYPE_CHECKING
from sqlmodel import Field, SQLModel, Relationship
from uuid import UUID
from uuid_extensions import uuid7
from datetime import datetime

if TYPE_CHECKING:
    from .phone_model import Phone

class Users(SQLModel, table=True):
    user_id: UUID = Field(primary_key=True, default_factory=uuid7)
    friendly_code: str = Field(nullable=False)
    fullname: str = Field(nullable=False)
    birthdate: datetime = Field(nullable=False)
    email: str = Field(nullable=False)
    password: str = Field(nullable=False)
    cpf: str = Field(nullable=False)
    created_at: datetime = Field(default_factory=datetime.now)
    user_photo: str | None = Field(default=None)
    is_deleted: bool = Field(default=False)


    phones: List["Phone"] = Relationship(back_populates="user")