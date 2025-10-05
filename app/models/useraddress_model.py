from sqlmodel import SQLModel, Field, Relationship
from uuid import UUID
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .user_model import Users
    from .address_model import Address

class UsersAddress(SQLModel, table=True):
    user_id: UUID = Field(foreign_key="users.user_id", primary_key=True)
    address_id: UUID = Field(foreign_key="address.address_id", primary_key=True)
    is_deleted: bool = Field(default=False, nullable=False)

    user: "Users" = Relationship(back_populates="addresses_link")
    address: "Address" = Relationship(back_populates="users_link")
