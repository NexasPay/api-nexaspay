from fastapi import APIRouter, HTTPException
from sqlalchemy.future import select
from app.models.wallet_model import Wallet
from app import dt
from app.dependencies import getDbData
from uuid_extensions import uuid7

router = APIRouter()

@router.get("wallet/{wallet_id}")
async def getAllWallets(wallet_id):
    return {"wallet_id": wallet_id, "money": 1000}

# @router.get("/wallet/")
# async def getAllWallets():
#     db = await getDbData()
#     return await db.execute(select(Wallet))


# @router.get("/wallet/{owner_id}")
# async def getWalletsFromUsers(owner_id: int):
#     db = await getDbData()
#     result = await db.execute(select(Wallet).where(Wallet.owner_id == owner_id))
#     wallets = result.scalars().all()
#     return wallets


# @router.post("/wallet/create")
# async def createWallet():
#     db = await getDbData()
    
#     owner_id = uuid7()
#     wallet = Wallet(address=f"wallet_{owner_id}_{int(dt.datetime.utcnow().timestamp())}", owner_id=owner_id)
#     db.add(wallet)
#     await db.commit()
#     await db.refresh(wallet)
#     return wallet

