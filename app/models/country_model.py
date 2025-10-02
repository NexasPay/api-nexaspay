from sqlmodel import Field, SQLModel
from uuid import UUID
from uuid_extensions import uuid7

class Country(SQLModel, table=True):
    country_id: UUID = Field(primary_key=True, default_factory=uuid7)
    name: str = Field(nullable=False)