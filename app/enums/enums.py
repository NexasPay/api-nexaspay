from enum import Enum

class WalletTypeEnum(Enum):
    DEFAULT = "DEFAULT"
    ENTERPRISE = "ENTERPRISE"
    CRYPTO = "CRYPTO"
    POINTS = "POINTS"
    INVESTMENT = "INVESTMENT"


class TransferTypeEnum(Enum):
    DEPOSIT = "DEPOSIT"
    PICKUP = "PICKUP"   # Saque
    PAYMENT = "PAYMENT"
    TRANSFER = "TRANSFER"


class PhoneTypeEnum(Enum):
    MOBILE = "MOBILE"
    BUSINESS = "BUSINESS"
    HOME = "HOME"


class ClassType(Enum):
    USERS = "USR"
    WALLET = "WLT"
    TRANSFER = "TRF"
    NEXAS = "NAI"