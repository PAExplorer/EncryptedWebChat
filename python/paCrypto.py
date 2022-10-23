#paCrypto
from cryptography.fernet import Fernet

def generateKey():
    return Fernet.generate_key()

def encryptString(message, key):
    fernet = Fernet(key)
    return fernet.encrypt(message.encode()) #in BYTES!

def decryptBytes(message, key):
    fernet = Fernet(key)
    return fernet.decrypt(message).decode() 