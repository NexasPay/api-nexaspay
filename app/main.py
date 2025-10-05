from fastapi import FastAPI
from sqlmodel import select
from app.models.user_model import Users
from app.db.session import init_db, SessionDep
from app.routers import user, wallet, transfer, auth
from fastapi.responses import RedirectResponse

app = FastAPI(title="Nexas Pay API v1", version='v1')

app.include_router(user.router, prefix="/api/v1/user", tags=["User Routes"])
app.include_router(auth.router, prefix="/api/v1/auth", tags=["OAuth2 Routes"])
app.include_router(wallet.router, prefix="/api/v1/wallet", tags=["Wallet Routes"])
app.include_router(transfer.router, prefix="/api/v1/transfer", tags=["Transfer Routes"])

@app.on_event("startup")
async def on_startup():
    init_db()

@app.get("/", name="Redireciona o usuário para o SwaggerUI")
async def root():
    return RedirectResponse("/docs")

@app.get("/health-check", name="Teste se a sua api está conectado ao banco de dados!")
def testUserDB(session: SessionDep):
    try:
        user = session.exec(select(Users)).first()
        return {"status": "OK"}
    except Exception as e:
        return {"status": "ERRO NA CONEXÃO", "Traceback": str(e)}