import asyncio

from config_reader import config

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.fernet import Fernet
import base64

#функция генерации ключа из пароля и соли
async def derive_key(password: str, salt: bytes) -> bytes: 
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
        backend = await asyncio.to_thread(default_backend)
    )
    return await asyncio.to_thread(lambda: base64.urlsafe_b64encode(
        kdf.derive(password.encode())))

# функция шифрования приватного ключа
async def encrypt_private_key(private_key: str, password: str) -> str:
    salt = bytes(await asyncio.to_thread(
        config.salt.get_secret_value),encoding='utf-8')#получаем соль из .env
    key = await derive_key(password, salt)
    cipher_suite = Fernet(key)
    encrypted_private_key = await asyncio.to_thread(
        lambda: cipher_suite.encrypt(private_key.encode()))  # Шифруем приватный ключ
    return  await asyncio.to_thread(lambda: encrypted_private_key.decode())

# функция дешифрования приватного ключа
async def decrypt_private_key(
        encrypted_private_key: str, password: str) -> str:
    #если ключ не верный, то мы не сможем расшифровать значение, из-за чего используя except мы вернем  None
    try:
        salt = bytes( await asyncio.to_thread(
            config.salt.get_secret_value),encoding='utf-8')#получаем соль из .env
        key = await derive_key(password, salt)
        cipher_suite = Fernet(key)
        decrypted_private_key = (
            await asyncio.to_thread(
                lambda: cipher_suite.decrypt(encrypted_private_key).decode()))
        return decrypted_private_key
    except:
        return None
    
    