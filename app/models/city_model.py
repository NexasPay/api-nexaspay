from sqlmodel import Field, SQLModel, Relationship
from uuid import UUID
from uuid_extensions import uuid7
from .state_model import State

class City(SQLModel, table=True):
    city_id: UUID = Field(primary_key=True, default_factory=uuid7)
    name: str = Field(nullable=False)
    state_id: UUID = Field(foreign_key="state.state_id", nullable=False)

    state: "State" = Relationship()