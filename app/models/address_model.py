from sqlmodel import Field, SQLModel, Relationship
from uuid import UUID
from uuid_extensions import uuid7
from .city_model import City

class Address(SQLModel, table=True):
    address_id: UUID = Field(primary_key=True, default_factory=uuid7)
    street: str = Field(nullable=False)
    number: str = Field(nullable=False)
    complement: str | None = Field(default=None)
    cep: str = Field(nullable=False)

    city_id: UUID = Field(foreign_key="City.city_id", nullable=False)

    city: "City" = Relationship()