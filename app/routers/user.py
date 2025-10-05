from fastapi import APIRouter, Form, File, UploadFile, HTTPException
from uuid import UUID
from app.models.user_model import Users, uuid7
from app.models.wallet_model import Wallet
from app.db.session import SessionDep
from app.models.walletType_model import Wallet_Type
from app.models.phone_model import Phone
from app.models.phoneType_model import PhoneType
from pydantic import BaseModel, Field
from typing import Annotated, Optional
from app.helpers import generateFriendlyCode, ClassType
from datetime import datetime
from sqlmodel import select
from app.internal.cryptography import encryptCPF
from app.internal.AuthUser import encryptPassword

router = APIRouter()

class ProfilePhotoModel(BaseModel):
    file: Annotated[bytes, File()]
    fileb: Annotated[UploadFile, File()]
    token: Annotated[str, File()]

class CreateUserFormData(BaseModel):
    fullname: str = Field(alias="NomeCompleto")
    birthdate: datetime = Field(alias="DataNascimento") 
    email: str = Field(alias="Email")
    phone: str = Field(alias="Celular")
    password: str = Field(alias="Senha")
    cpf: str = Field(alias="CPF")

@router.get("/{userFriendlyCode}", name="Obtendo informações do usuário")
async def getUserDetails(userFriendlyCode: str, session: SessionDep):
    statement = select(Users).where(Users.friendly_code == userFriendlyCode)
    user = session.exec(statement).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user
    

@router.post("/create", name="Criando novo usuário")
async def createNewUser(data: Annotated[CreateUserFormData, Form()], session: SessionDep):
    
    newUser = Users(
        user_id=uuid7(),
        friendly_code=generateFriendlyCode(ClassType.USERS),
        fullname=data.fullname,
        birthdate=data.birthdate,
        email=data.email,
        password=encryptPassword(data.password),
        cpf=encryptCPF(data.cpf),
        created_at=datetime.now(),
        user_photo=None,
        is_deleted=False
    )
    # userPhone = Phone(phone_id=uuid7(), number=data.phone, is_primary=False, user_id=newUser.user_id)
    
    session.add(newUser)
    session.commit()
    session.refresh(newUser)
    
    return newUser
