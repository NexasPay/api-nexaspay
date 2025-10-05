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



@router.get("/getid/{walletTypeName}")
async def getWalletTypeByName(session, walletTypeName: Literal["Default", "Enterprise", "Crypto", "Investment"] = "Default"):
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


@router.patch("/addMoney/{walletFriendlyCode}", name="Adicione dinheiro a carteira de um usuário")
async def addMoneyToUserWallet(walletFriendlyCode: str, money: float, session: SessionDep):
    try:
        statement = select(Wallet).where(Wallet.friendly_code == walletFriendlyCode)
        wallet: Wallet = (await findWalletByFriendlyCode(walletFriendlyCode=walletFriendlyCode, session=session))["wallet"]

        wallet.money += money

        session.add(wallet)
        session.commit()
        session.refresh(wallet)

        return {"is_created": True, "wallet": wallet}
    except HTTPException:
        raise
    except Exception as e:
        print(e)
