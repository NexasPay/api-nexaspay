from cryptography.hazmat.primitives.ciphers.aead import AESGCM
import base64
from dotenv import load_dotenv
from os import getenv
            
def encryptCPF(cpf: str) -> str:
    """
    Encrypt CPF from user
    """
    if not cpf.isnumeric():
        raise Exception("CPF deve conter somente números")
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