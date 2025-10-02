from fastapi import APIRouter, HTTPException
from app.dependencies import getDbData
from sqlalchemy.future import select
from app.models.wallet_model import Wallet
from app.models.transfer_model import Transfer

router = APIRouter()

# Only for test
@router.get("/transaction/{transfer_id}")
async def readTransaction(transfer_id: int):
    return {"transfer_id": transfer_id}
    


# @router.post("/transaction/create")
# async def createTransaction(from_wallet: str, to_wallet: str, amount: float):
#     db = await getDbData()

#     result_from = db.execute(select(Wallet).where(Wallet.address == from_wallet))
#     result_to = db.execute(select(Wallet).where(Wallet.address == to_wallet))

#     await result_from
#     await result_to
#     w_from = result_from.scalar_one_or_none()
#     w_to = result_to.scalar_one_or_none()

#     if not w_from or not w_to:
#         raise HTTPException(status_code=404, detail="Transação não encontrada")
#     if w_from.balance < amount:
#         raise HTTPException(status_code=400, detail="Saldo insuficiente")

    
#     w_from.balance -= amount
#     w_to.balance += amount


#     transaction = Transaction(
#         from_wallet=from_wallet,
#         to_wallet=to_wallet,
#         amount=amount,
#         status="completed",
#         created_at=dt.datetime.utcnow()
#     )
#     db.add(transaction)
#     await db.commit()
#     await db.refresh(transaction)
#     return transaction
