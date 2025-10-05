from fastapi import APIRouter, HTTPException
from app.dependencies import getDbData
from app.db.session import SessionDep
from sqlalchemy import select
from app.helpers import generateFriendlyCode, ClassType
from app.models.wallet_model import Wallet
from app.models.transfer_model import Transfer
from app.models.transferType_model import TransferType
from app.routers.wallet import findWalletByUUID, cashInToUserWallet, getWalletTypeByName, cashOutFromUserWallet
from uuid import UUID
from typing import Literal
from uuid_extensions import uuid7
from datetime import datetime

router = APIRouter()

@router.post("/{transferType}/from/{originWalletId}/{originValue}/to/{targetWalletId}", name="Realize transferências entre Carteiras")
async def makePaymentToTarget(transferType: Literal["TRANSFER", "CRYPTO", "PIX"], originWalletId: UUID, originValue: int, targetWalletId: UUID, session: SessionDep):
    try:
        if originValue < 0:
            raise HTTPException(status_code=400, detail="Valor de pagamento inválido.")

        targetWallet: Wallet = await findWalletByUUID(walletUUID=targetWalletId, session=session)
        originWallet: Wallet = await findWalletByUUID(walletUUID=originWalletId, session=session)

        await cashOutFromUserWallet(originWallet.friendly_code, originValue, session)
        await cashInToUserWallet(targetWallet.friendly_code, originValue, session)

        result = session.exec(select(TransferType).where(TransferType.transfer_type_name == transferType)).scalars().first()


        if not result:
            raise HTTPException(status_code=404, detail=f"Tipo de transferência '{transferType}' não encontrado.")


        transferinfos = Transfer(
            transfer_id=uuid7(),
            friendly_code=generateFriendlyCode(ClassType.TRANSFER),
            amount=originValue,
            paid_at=datetime.now(),
            is_scheduled=False,
            scheduled_date=None,
            origin_wallet_id=originWallet.wallet_id,
            target_wallet_id=targetWallet.wallet_id,
            transfer_type_id=result.transfer_type_id
        )

        session.add(transferinfos)
        session.commit()
        session.refresh(transferinfos)

        return {
                "transferValid": True, 
                "originWalletCurrentMoney": originWallet.money, 
                "targetWalletCurrentMoney": targetWallet.money, 
                "TransferInfos": transferinfos
            }
    except HTTPException:
        raise
    except Exception as e:
        print(e)
        raise

@router.post("/invest/{originWalletID}/{value}", name="Realize transferências entre suas carteiras de investimentos")
async def sendToInvestmentAccount(originWalletID: UUID, value: int):
    return {"message": "Em construção"}