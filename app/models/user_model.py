from typing import List, TYPE_CHECKING
from sqlmodel import Field, SQLModel, Relationship
from uuid import UUID
from typing import Optional
from uuid_extensions import uuid7
from pydantic import EmailStr
from datetime import datetime
from app.models.useraddress_model import UsersAddress

if TYPE_CHECKING:
    from .phone_model import Phone

class Users(SQLModel, table=True):
    user_id: UUID = Field(primary_key=True, default_factory=uuid7)
    friendly_code: str = Field(nullable=False)
    fullname: str = Field(nullable=False)
    birthdate: datetime = Field(nullable=False)
    email: EmailStr = Field(nullable=False)
    password: str = Field(nullable=False)
    cpf: str = Field(nullable=False)
    score: int = Field(nullable=False, default_factory=lambda: 0)
    created_at: datetime = Field(default_factory=datetime.now)
    user_photo: str | None = Field(default=None)
    is_deleted: bool = Field(default=False)

    addresses_link: List["UsersAddress"] = Relationship(back_populates="user")
    addresses: List["Address"] = Relationship(link_model=UsersAddress)
    phones: List["Phone"] = Relationship(back_populates="user", sa_relationship_kwargs={"foreign_keys": "[Phone.user_id]"})