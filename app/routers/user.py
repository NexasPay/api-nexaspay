from fastapi import APIRouter, Form, File, UploadFile, HTTPException
from uuid import UUID
from app.models.user_model import Users, uuid7
from app.models.wallet_model import Wallet
from app.db.session import SessionDep
from app.models.walletType_model import WalletType
from app.models.phone_model import Phone
from app.models.phoneType_model import PhoneType
from app.models.address_model import Address
from pydantic import BaseModel, Field
from typing import Annotated, Optional, Literal, List
from app.helpers import generateFriendlyCode, ClassType, calculateScorePoints, converDatetimeDelta
from datetime import datetime
from sqlmodel import select
from app.internal.cryptography import encryptCPF
from app.internal.AuthUser import encryptPassword
from app.models.useraddress_model import UsersAddress
from app.routers.wallet import getWalletTypeByName

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

@router.get("/{userFriendlyCode}", name="Obtendo detalhes sobre o cliente Nexas Pay")
async def getUserDetails(userFriendlyCode: str, session: SessionDep):
    statement = select(Users).where(Users.friendly_code == userFriendlyCode)
    user = session.exec(statement).first()
    if not user:
        raise HTTPException(status_code=404, detail="Usuário não encontrado.")
    return user
    
@router.get("/score/{userFriendlyCode}", name="Procurando pelo Score de um usuário a partir de seu friendlyCode")
async def getScoreFromUserCode(userFriendlyCode: str, session: SessionDep):
    statement = select(Users).where(Users.friendly_code == userFriendlyCode)
    user: Users = session.exec(statement).first()
    if not user:
        raise HTTPException(status_code=404, detail="Usuário não encontrado.", valid=False)
    return user.score

@router.get("/wallets/{userFriendlyCode}", name="Procurando pela carteira de um usuário")
async def getWalletsFromUsers(userFriendlyCode: str, session: SessionDep):
    
    try:
        user: User = session.exec(select(Users).where(Users.friendly_code == userFriendlyCode)).first()
        
        if not user:
            raise HTTPException(status_code=400, detail="Usuário não encontrado")
        
        statement = select(Wallet).where(Wallet.user_id == user.user_id)
        wallets: List[Wallet] = session.exec(statement)

        if len([wallets]):
            raise HTTPException(status_code=400, detail=f"O usuário {user.fullname} não possuí carteiras")
        
        return wallets
    except Exception as e:
        print(e)
        raise

@router.post("/create", name="Criando novo usuário")
async def createNewUser(data: Annotated[CreateUserFormData, Form()], session: SessionDep):
    try:
        if ((datetime.today() - data.birthdate).days // 365) < 18 or data.birthdate.year < 1930:
            raise HTTPException(status_code=400, detail="Data de aniversário inválida. Você não possuí a idade adequada para acessar o nosso sistema!")

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
        #uuid = uuid7()
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
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"Ocorreu um erro ao criar o usuário: {e}")
        #raise

@router.post("/create/wallet/{userFriendlyCode}", name="Criando uma nova carteira para o usuário")
async def createNewWalletForUser(userFriendlyCode: str, session: SessionDep, walletType: Literal["Default", "Enterprise", "Crypto", "Investment"] = "Default"):
    try:
        user = await getUserDetails(userFriendlyCode, session)

        walletType_id = (await getWalletTypeByName(session=session, walletTypeName=walletType)).wallet_type_id
        walletTypeStatement = select(Wallet).where((user.user_id == Wallet.user_id) & (Wallet.wallet_type_id == walletType_id))
        userWallets = session.exec(walletTypeStatement).first()


        if userWallets:
            raise HTTPException(status_code=409, detail=f"O usuário já possui esse tipo de carteira '{walletType}'")

        wallet = Wallet(
            wallet_id = uuid7(),
            friendly_code = generateFriendlyCode(ClassType.WALLET),
            wallet_type_id=walletType_id,
            user_id=user.user_id,
            money=0,
            is_deleted=False
        )

        session.add(wallet)
        session.commit()
        session.refresh(wallet)

        return {"valid": False, "wallet": wallet}
    except HTTPException:
        raise
    except Exception as e:
        print(e)
        raise HTTPException(status_code=404, detail="Ocorreu um erro durante o processo de criar uma carteira")

@router.patch("/score/increase/{userFriendlyCode}/", name="Aumente o score partindo de um friendly code")
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


