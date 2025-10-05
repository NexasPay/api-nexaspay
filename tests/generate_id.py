from dotenv import load_dotenv
from os import getenv
load_dotenv()
print(getenv("NONCE"))
print(len(getenv("NONCE")))
bytes.fromhex(getenv("NONCE"))

from app.internal.cryptography import decryptCPF

a = decryptCPF()