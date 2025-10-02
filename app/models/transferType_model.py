from sqlmodel import Field, SQLModel
from uuid import UUID
from uuid_extensions import uuid7
from .enums_model import TransferTypeEnum

class TransactionType(SQLModel, table=True):
    transaction_type_id: UUID = Field(primary_key=True, default_factory=uuid7)
    name: TransferTypeEnum = Field(default=TransferTypeEnum.DEPOSIT)