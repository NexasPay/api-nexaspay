from fastapi import FastAPI
from app.db.session import init_db
from app.routers import auth, wallet, transfer


app = FastAPI()

app.include_router(auth.router, prefix="/auth", tags=["Auth"])
app.include_router(wallet.router, prefix="/wallet", tags=["Wallet"])
app.include_router(transfer.router, prefix="/transaction", tags=["Transfer"])

@app.on_event("startup")
async def on_startup():
    await init_db()
