from sqlmodel import Field, SQLModel
from uuid import UUID
from uuid_extensions import uuid7
from .enums_model import PhoneTypeEnum

class PhoneType(SQLModel, table=True):
    phone_type_id: UUID = Field(primary_key=True, default_factory=uuid7)
    name: PhoneTypeEnum = Field(default=PhoneTypeEnum.HOME)
    is_whatsapp: bool = Field(default=False)

