from typing import TYPE_CHECKING
from sqlmodel import Field, SQLModel, Relationship
from uuid import UUID
from uuid_extensions import uuid7
from .phoneType_model import PhoneType

if TYPE_CHECKING:
    from .user_model import User

class Phone(SQLModel, table=True):
    phone_id: UUID = Field(primary_key=True, default_factory=uuid7)
    number: str = Field(nullable=False)
    is_primary: bool = Field(default=False)

    user_id: UUID = Field(foreign_key="User.user_id", nullable=False)
    phone_type_id: UUID = Field(foreign_key="PhoneType.phone_type_id", nullable=False)

    user: "User" = Relationship(back_populates="phones")
    phone_type: "PhoneType" = Relationship()