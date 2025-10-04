from fastapi import FastAPI
from app.db.session import init_db
from app.routers import user, wallet, transfer
from fastapi.responses import RedirectResponse

app = FastAPI(title="Nexas Pay API v1")

app.include_router(user.router, prefix="/user", tags=["User"])
app.include_router(wallet.router, prefix="/wallet", tags=["Wallet"])
app.include_router(transfer.router, prefix="/transfer", tags=["Transfer"])

@app.on_event("startup")
async def on_startup():
    await init_db()

@app.get("/")
async def root():
    return RedirectResponse("/docs")

