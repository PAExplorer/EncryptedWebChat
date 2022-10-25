#paCrypto

import base64
from re import X
from cryptography.fernet import Fernet 
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

salt = b'\xe8\x19\x11 .k\xde\xce\xd0\xb5B\x9c\xa5\xa8\xb7\x07' #This should probably be unique, but whatever.

def encryptString(message= "Test message", password = "12356"):
    if type(password) == type("string"):
        password = bytes(password, 'utf-8')
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=390000,
    )
    key = base64.urlsafe_b64encode(kdf.derive(password))
    fern = Fernet(key)
    if type(message) == type("string"):
        message = bytes(message, 'utf-8')
    return fern.encrypt(message)

def decryptBytes(message = b'gAAAAABjVz5Xxm8l1ARWzPROFIcTNYgQWWighAhUCS0zNre2tjo7iysjupDpteHq9kXGyHV0o-BV6Rg456746ENlD-qDerWO3w==', password = "12356"):
    if type(password) == type("string"):
        password = bytes(password, 'utf-8')
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=390000,
    )
    key = base64.urlsafe_b64encode(kdf.derive(password))
    fern = Fernet(key)
    if type(message) == type("string"):
        message = bytes(message, 'utf-8')
    return str(fern.decrypt(message), 'utf-8')

#Test Script
#generateKey()
#x = encryptString("ABCDEFGHIJKLMNOPQRSTUVWXYZ!?!@#$%^&*()asdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdf")

#y = decryptBytes(x)
#print(y)
