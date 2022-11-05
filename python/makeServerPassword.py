import pickle, os
from paCrypto import *

definition = "Lorem ipsum dolor sit amet, consectetuer adipiscing elit, sed diam nonummy nibh."

def checkLockFile():
    if os.path.exists('lock.dat'):
        return True
    else:
        print("[WARNING] Lock file not found")
        return False

def newPass():
    x = input("Please enter a new password for the server:")
    if type(x) != type("String"):
        x = str(x, 'utf-8')
    lock = encryptString(definition, x)
    with open('lock.dat', 'wb') as f:
        pickle.dump(lock, f)
        print("password lock saved to file.")
        f.close()

def checkPass(inPass):
    try:
        with open('lock.dat', 'rb') as f:
            #Load the data from the save file
            lock = pickle.load(f)
            f.close()
        x = decryptBytes(lock, inPass)
        if x == definition:
            return True
            print("Password accepted.")
        else:
            return False
            print("Password not accepted.")
    except:
        print("An error has occured")
        return False

def readFile():
    x = checkLockFile()
    if x is True:
        with open('lock.dat', 'rb') as f:
            #Load the data from the save file
            lock = pickle.load(f)
            f.close()
        print(lock)
    else:
        print("[SYSTEM] File not found.")

if __name__ == "__main__":
    print("=========================")
    print("   paNetSet v0.0.0")
    print("=========================")
    while True:
        x = input("Enter command:")
        match x:
            case "write":
                newPass()
            case "check":
                pWord = input("Please input a password:")
                x = checkPass(pWord)
                if x == True:
                    print("Password accepted.")
                else:
                    print("Password NOT accepted.")
            case "read":
                readFile()
            case "exit":
                exit()
            case _:
                print("Commands are:")
                print("write = Write a new port for the system to use.")
                print("check = Try the password on the lock")
                print("read = read the lock")
                print("exit = close the program")