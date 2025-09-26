from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.db import get_db
from app.models import Wallet

router = APIRouter()

@router.post("/")
async def create_wallet(owner_id: int, db: AsyncSession = Depends(get_db)):
    wallet = Wallet(address=f"wallet_{owner_id}_{int(datetime.datetime.utcnow().timestamp())}", owner_id=owner_id)
    db.add(wallet)
    await db.commit()
    await db.refresh(wallet)
    return wallet

@router.get("/{owner_id}")
async def get_wallets(owner_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Wallet).where(Wallet.owner_id == owner_id))
    wallets = result.scalars().all()
    return wallets
