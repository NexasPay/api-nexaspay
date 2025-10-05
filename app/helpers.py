from pydantic import BaseModel, Field
from app.enums.enums import ClassType
from app.models.transferType_model import TransferType
from app.db.session import SessionDep
from random import randint
from fastapi import HTTPException
from sqlmodel import select
from uuid import UUID
import math
from datetime import datetime

def generateFriendlyCode(codeType: ClassType):
    """
    Generate random FriendlyCode
    """
    code = randint(100000, 999999)
    friendlyCode = f'{codeType.value}{code}'
    return friendlyCode


def calculateScorePoints(value: float, transferName: str, session: SessionDep) -> int:
    try:
        type_variables = {
            "pickup": 0.3,
            "deposit": 0.6,
            "transfer": 0.7,
            "pix": 0.8,
            "invest": 1.2,
            "crypto": 1.4
        }.get(transferName.lower(), 1.0)

        newPoints = (math.sqrt(value) / 4) * (type_variables * 1.2)

        points = min(newPoints, 1000)

        return round(points, 0)
    except Exception as e:
        print(e)
        raise HTTPException(status_code=400, detail="Operação de pontos teve falha.")

def converDatetimeDelta(delta):
    totalDays = delta.days
    years = totalDays // 365
    months = (totalDys % 365) // 30
    days = (totalDays % 365) % 30
    return datetime(years, months, days)

def validate_birth_date(birth_date: datetime):
    today = datetime.now()
    age = today.year - birth_date.year - (
        (today.month, today.day) < (birth_date.month, birth_date.day)
    )

    if age < 18 or birth_date.year < 1930:
        raise
    return age