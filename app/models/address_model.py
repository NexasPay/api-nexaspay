from sqlmodel import Field, SQLModel, Relationship
from uuid import UUID
from typing import List
from uuid_extensions import uuid7
from .city_model import City

class Address(SQLModel, table=True):
    address_id: UUID = Field(primary_key=True, default_factory=uuid7)
    street: str = Field(nullable=False)
    address_number: str = Field(nullable=False)
    complement: str | None = Field(default=None)
    cep: str = Field(nullable=False)

    city_id: UUID = Field(foreign_key="city.city_id", nullable=True)

    city: "City" = Relationship()
    users_link: List["UsersAddress"] = Relationship(back_populates="address")