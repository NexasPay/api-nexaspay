from pydantic import BaseModel, Field
from app.enums.enums import ClassType
from random import randint
from sqlmodel import select


def generateFriendlyCode(codeType: ClassType):
    """
    Generate random FriendlyCode
    """
    code = randint(100000, 999999)
    friendlyCode = f'{codeType.value}{code}'
    return friendlyCode
