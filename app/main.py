from fastapi import FastAPI
from sqlmodel import select
from app.models.user_model import Users
from app.db.session import init_db, SessionDep
from app.routers import user, wallet, transfer, auth
from fastapi.responses import RedirectResponse

app = FastAPI(title="Nexas Pay API v1")

app.include_router(user.router, prefix="/user", tags=["User"])
app.include_router(auth.router, prefix="/auth", tags=["Auth"])
app.include_router(wallet.router, prefix="/wallet", tags=["Wallet"])
app.include_router(transfer.router, prefix="/transfer", tags=["Transfer"])

@app.on_event("startup")
async def on_startup():
    init_db()

@app.get("/")
async def root():
    return RedirectResponse("/docs")

@app.get("/debug-db")
def debug_db(session: SessionDep):
    try:
        user = session.exec(select(Users)).first()
        return {"status": "ok", "user_found": bool(user)}
    except Exception as e:
        return {"status": "error", "detail": str(e)}