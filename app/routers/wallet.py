from fastapi import APIRouter, HTTPException
from sqlalchemy.future import select
from app.models.wallet_model import Wallet
from app.models.walletType_model import WalletType
from app import dt
from typing import Literal
from sqlmodel import select
from app.dependencies import getDbData
from uuid_extensions import uuid7

router = APIRouter()

@router.get("/{wallet_id}")
async def getWalletsFromUsers(wallet_id):
    return 


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
