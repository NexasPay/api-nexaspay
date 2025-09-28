from fastapi import FastAPI
from app.db.session import engine, Base
from app.routers import auth, wallet, transaction

app = FastAPI(title="Carteira Digital Inteligente")


app.include_router(auth.router, prefix="/auth", tags=["Auth"])
app.include_router(wallet.router, prefix="/wallet", tags=["Wallet"])
app.include_router(transaction.router, prefix="/transaction", tags=["Transaction"])

@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
