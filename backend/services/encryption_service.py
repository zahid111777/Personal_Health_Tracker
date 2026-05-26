import os
from cryptography.fernet import Fernet
from dotenv import load_dotenv

load_dotenv()

_fernet_key = os.getenv("FERNET_KEY")
if not _fernet_key:
    _fernet_key = Fernet.generate_key().decode()
    print(f"WARNING: No FERNET_KEY set. Generated temporary key: {_fernet_key}")
    print("Set FERNET_KEY in your .env file for persistent encryption.")

_fernet = Fernet(_fernet_key.encode() if isinstance(_fernet_key, str) else _fernet_key)


def encrypt_value(value: str) -> str:
    if not value:
        return ""
    return _fernet.encrypt(value.encode()).decode()


def decrypt_value(encrypted_value: str) -> str:
    if not encrypted_value:
        return ""
    return _fernet.decrypt(encrypted_value.encode()).decode()


def get_fernet_key() -> str:
    return _fernet_key
