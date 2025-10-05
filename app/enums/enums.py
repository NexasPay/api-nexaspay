from enum import Enum

class WalletTypeEnum(Enum):
    DEFAULT = "DEFAULT"
    ENTERPRISE = "ENTERPRISE"
    CRYPTO = "CRYPTO"
    INVESTMENT = "INVESTMENT"


class TransferTypeEnum(Enum):
    DEPOSIT = "DEPOSIT"
    PICKUP = "PICKUP"
    TRANSFER = "TRANSFER"
    CRYPTO = "CRYPTO"
    INVEST = "INVEST"
    PIX = "PIX"


class PhoneTypeEnum(Enum):
    MOBILE = "MOBILE"
    BUSINESS = "BUSINESS"
    HOME = "HOME"


class ClassType(Enum):
    USERS = "USR"
    WALLET = "WLT"
    TRANSFER = "TRF"
    NEXAS = "NAI"