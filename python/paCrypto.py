#paCrypto

import base64
from re import X
from cryptography.fernet import Fernet 
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

salt = b'\xe8\x19\x11 .k\xde\xce\xd0\xb5B\x9c\xa5\xa8\xb7\x07' #This should probably be unique, Feel free to change it on both your clients and servers if you feel the need.

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
    try:
        bMessage = fern.encrypt(message)
        return bMessage
    except:
        return b"Encryption Error"

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
    try:
        msgReturn = str(fern.decrypt(message), 'utf-8')
        return msgReturn
    except:
        return "Decryption error"

if __name__ == "__main__":
    #Test Script
    x = encryptString("ABCDEFGHIJKLMNOPQRSTUVWXYZ!?!@#$%^&*()asdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdf")
    print("The encrypted data looks like this:")
    print(x)
    y = decryptBytes(x)
    print("The unencrypted data looks like this:")
    print(y)
