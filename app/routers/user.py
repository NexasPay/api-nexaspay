from fastapi import APIRouter, Form, File, UploadFile, HTTPException
from uuid import UUID
from app.models.user_model import Users, uuid7
from app.models.wallet_model import Wallet
from app.db.session import SessionDep
from app.models.walletType_model import Wallet_Type
from app.models.phone_model import Phone
from app.models.phoneType_model import PhoneType
from app.models.address_model import Address
from pydantic import BaseModel, Field
from typing import Annotated, Optional, Literal
from app.helpers import generateFriendlyCode, ClassType, calculateScorePoints
from datetime import datetime
from sqlmodel import select
from app.internal.cryptography import encryptCPF
from app.internal.AuthUser import encryptPassword
from app.models.useraddress_model import UsersAddress

router = APIRouter()

class ProfilePhotoModel(BaseModel):
    file: Annotated[bytes, File()]
    fileb: Annotated[UploadFile, File()]
    token: Annotated[str, File()]

class CreateUserFormData(BaseModel):
    fullname: str = Field(alias="Nome Completo")
    birthdate: datetime = Field(alias="Data Nascimento") 
    street: str = Field(alias="Rua")
    complement: str = Field(alias="Complemento")
    address_number: str = Field(alias="Número")
    cep: str = Field(alias="CEP")
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
    
    try:

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
        uuid = 'c1266dad-16f7-44d9-9009-f5510378fb2d'
        userPhone = Phone(phone_id=uuid7(), phone_number=data.phone, is_primary=False, user_id=newUser.user_id, phone_type_id=uuid)
        userAddress = Address(address_id=uuid7(), street=data.street, complement=data.complement, address_number=data.address_number, cep=data.cep, city_id=None)
        userAddressTable = UsersAddress(user_id=newUser.user_id, address_id=userAddress.address_id)

        session.add(newUser)
        session.add(userPhone)
        session.add(userAddress)
        session.add(userAddressTable)
        session.commit()
        session.refresh(newUser)
        
        return newUser
    except Exception as e:
        print(e)
        raise HTTPException(status_code=404, detail=f"Ocorreu um erro ao criar o usuário")

@router.get("/score/{userFriendlyCode}")
async def getScoreFromUserCode(userFriendlyCode: str, session: SessionDep):
    statement = select(Users).where(Users.friendly_code == userFriendlyCode)
    user: Users = session.exec(statement).first()
    if not user:
        raise HTTPException(status_code=404, detail="Usuário não encontrado.", valid=False)
    return user.score

@router.put("/score/{userFriendlyCode}/increase")
async def increaseScorePoints(userFriendlyCode:str, paymentValue: float, session: SessionDep, transferType: Literal["Deposit", "Pix", "Pickup", "Transfer", "Crypto", "Invest"] = "Pix"):
    statement = select(Users).where(Users.friendly_code == userFriendlyCode)
    user: Users = session.exec(statement).first()
    if not user:
        raise HTTPException(status_code=404, detail='Usuário não encontrado')

    if paymentValue <= 0 or paymentValue > 50000:
        raise HTTPException(status_code=400, detail='Valor inválido para operação')

    user.score += calculateScorePoints(value=paymentValue, transferName=transferType, session=session)

    session.add(user)
    session.commit()
    session.refresh(user)
    return {"Score Atual": user.score, "Valid": True} 