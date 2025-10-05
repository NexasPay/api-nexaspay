from cryptography.hazmat.primitives.ciphers.aead import AESGCM
import base64
from dotenv import load_dotenv
from os import getenv
from fastapi import HTTPException
            
def encryptCPF(cpf: str) -> str:
    """
    Encrypt CPF from user
    """
    if not cpf.isnumeric():
        raise HTTPException(status_code=400, detail="CPF deve conter somente números")
    if len(cpf) < 11:
        raise HTTPException(status_code=400, detail="CPF deve conter 11 caractéres exatas")
    load_dotenv()
    hashKey = bytes.fromhex(getenv('SECRET_HASH_KEY')) 
    nonce = bytes.fromhex(getenv('NONCE'))
    aesgcm = AESGCM(hashKey)

    return base64.b64encode(aesgcm.encrypt(nonce, cpf.encode(), None)).decode()

def decryptCPF(cpf: str) -> str:
    """
    Decrypt CPF document 
    """
    load_dotenv() 
    hashKey = bytes.fromhex(getenv('SECRET_HASH_KEY')) 
    nonce = bytes.fromhex(getenv('NONCE'))
    aesgcm = AESGCM(hashKey)

    return aesgcm.decrypt(nonce, base64.b64decode(cpf), None).decode()