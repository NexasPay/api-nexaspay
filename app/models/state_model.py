from sqlmodel import Field, SQLModel, Relationship
from uuid import UUID
from uuid_extensions import uuid7
from .country_model import Country

class State(SQLModel, table=True):
    state_id: UUID = Field(primary_key=True, default_factory=uuid7)
    name: str = Field(nullable=False)
    uf: str = Field(nullable=False)

    country_id: UUID = Field(foreign_key="Country.country_id", nullable=False)

    country: "Country" = Relationship()