from fastapi import APIRouter, Form, File, UploadFile
from uuid import UUID
from app.models.user_model import User, uuid7
from app.models.wallet_model import Wallet
from app.db.session import async_session
from app.models.walletType_model import Wallet_Type
from app.models.phone_model import Phone
from app.models.phoneType_model import PhoneType
from pydantic import BaseModel, Field
from typing import Annotated, Optional
from app.helpers import generateFriendlyCode, ClassType
from datetime import datetime
from app.internal.cryptography import encryptCPF
from app.internal.AuthUser import encryptPassword

router = APIRouter()

class ProfilePhotoModel(BaseModel):
    file: Annotated[bytes, File()]
    fileb: Annotated[UploadFile, File()]
    token: Annotated[str, File()]

class CreateUserFormData(BaseModel):
    full_name: str = Field(alias="NomeCompleto")
    birhtdate: datetime = Field(alias="DataNascimento")
    email: str = Field(alias="Email")
    phone: str = Field(alias="Celular")
    password: str = Field(alias="Senha")
    cpf: str = Field(alias="CPF")

@router.get("/{userId}", response_model=User, name="Obtendo informações do usuário")
async def getUserDetails(userId: UUID):
    pass

@router.post("/create", name="Criando novo usuário")
async def createNewUser(data: Annotated[CreateUserFormData, Form()]):
    
    newUser = User(
        user_id=uuid7(),
        friendly_code=generateFriendlyCode(ClassType.USERS),
        full_name=data.full_name,
        birthdate=data.birhtdate,
        email=data.email,
        password=encryptPassword(data.password),
        cpf=encryptCPF(data.cpf),
        created_at=datetime.now(),
        profile_photo=None,
        is_deleted=False
    )
    userPhone = Phone(phone_id=uuid7(), number=data.phone, is_primary=False, user_id=newUser.user_id)
    
    async with async_session() as session:
        session.add(newUser)
        await session.commit()
        await session.refresh(newUser)
    
    return newUser
