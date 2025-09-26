from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.db import get_db
from app.models import Wallet, Transaction
import datetime

router = APIRouter()

@router.post("/")
async def create_transaction(from_wallet: str, to_wallet: str, amount: float, db: AsyncSession = Depends(get_db)):
 
    result_from = await db.execute(select(Wallet).where(Wallet.address == from_wallet))
    w_from = result_from.scalar_one_or_none()
    result_to = await db.execute(select(Wallet).where(Wallet.address == to_wallet))
    w_to = result_to.scalar_one_or_none()

    if not w_from or not w_to:
        raise HTTPException(status_code=404, detail="Wallet not found")
    if w_from.balance < amount:
        raise HTTPException(status_code=400, detail="Saldo insuficiente")

    
    w_from.balance -= amount
    w_to.balance += amount


    tx = Transaction(
        from_wallet=from_wallet,
        to_wallet=to_wallet,
        amount=amount,
        status="completed",
        created_at=datetime.datetime.utcnow()
    )
    db.add(tx)
    await db.commit()
    await db.refresh(tx)
    return tx
