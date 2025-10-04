from sqlmodel import Field, SQLModel, Relationship
from uuid import UUID
from typing import List
from uuid_extensions import uuid7
from .enums_model import PhoneTypeEnum

class PhoneType(SQLModel, table=True):
    phone_type_id: UUID = Field(primary_key=True, default_factory=uuid7)
    name: str = Field(default=PhoneTypeEnum.HOME)
    is_whatsapp: bool = Field(default=False)

    phones: List["Phone"] = Relationship(back_populates="phone_type")

