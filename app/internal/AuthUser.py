from fastapi.security import OAuth2AuthorizationCodeBearer
from pwdlib import PasswordHash

password_hash = PasswordHash.recommended()

def encryptPassword(password: str) -> str:
    """
    Encrypt Password from user
    """
    return password_hash.hash(password)

def checkPassword(possiblePassword:str, passwordHash: str) -> bool:
    """
    Verify if the password is valid
    """
    return password_hash.verify(possiblePassword, passwordHash)