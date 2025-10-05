from fastapi import APIRouter, HTTPException
from sqlalchemy.future import select
from app.models.wallet_model import Wallet
from app.db.session import SessionDep
from app.models.walletType_model import WalletType
from app import dt
from typing import Literal
from sqlmodel import select
from app.dependencies import getDbData
from uuid_extensions import uuid7

router = APIRouter()



@router.get("/getid/{walletTypeName}", name="Obtenha o UUID do tipo da carteira partindo do seu nome de tipo")
async def getWalletTypeByName(walletTypeName: Literal["Default", "Enterprise", "Crypto", "Investment"], session: SessionDep):
    try:
        statement = select(WalletType).where(WalletType.wallet_type_name == walletTypeName.upper())
        walletTypeId = session.exec(statement).first()
        if not walletTypeId.wallet_type_id:
            raise HTTPException(status_code=400, detail="Tipo de carteira inválido")
        return walletTypeId
    except Exception as e:
        print(e)
        raise

    return None

@router.get("/find/{walletFriendlyCode}", name="Procure uma carteira pelo seu Friendly Code")
async def findWalletByFriendlyCode(walletFriendlyCode: str, session: SessionDep):
    statement = select(Wallet).where(Wallet.friendly_code == walletFriendlyCode)
    wallet = session.exec(statement).first()

    if not wallet:
        raise HTTPException(status_code=400, detail="A carteira não foi encontrada no sistema")

    return {"valid": True, "wallet": wallet}


@router.patch("/cashin/{walletFriendlyCode}", name="Adicione dinheiro a carteira de um usuário")
async def cashInToUserWallet(walletFriendlyCode: str, money: float, session: SessionDep):
    try:
        wallet: Wallet = (await findWalletByFriendlyCode(walletFriendlyCode=walletFriendlyCode, session=session))["wallet"]
        
        if money <= 0 or money > 10000000:
            raise HTTPException(status_code=400, detail="O valor que está tentando colocar ultrapassa ou é abaixo dos nossos limites")
        
        wallet.money += money

        session.add(wallet)
        session.commit()
        session.refresh(wallet)

        return {"validOperation": True, "wallet": wallet}
    except HTTPException:
        raise
    except Exception as e:
        print(e)

@router.patch("/cashout/{userFriendlyCode}", name="Remova dinheiro da carteira partindo de um FriendlyCode")
async def cashOutFromUserWallet(walletFriendlyCode: str, money: float, session: SessionDep):
    try:
        wallet: Wallet = (await findWalletByFriendlyCode(walletFriendlyCode=walletFriendlyCode, session=session))["wallet"]

        if wallet.money - money < 0:
            raise HTTPException(status_code=400, detail="O Saldo da sua conta não pode ficar negativo.")

        wallet.money -= money

        session.add(wallet)
        session.commit()
        session.refresh(wallet)

        return {"validOperation": True, "wallet": wallet}
    except HTTPException:
        raise
    except Exception as e:
        print(e)