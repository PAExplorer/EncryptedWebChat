import pickle, os, re
from PASearches import *

def checkSettFile():
    if os.path.exists('NetworkSettings.dat'):
        return True
    else:
        print("[WARNING] Network settings file not found, please make one if needed. Otherwise the default port is: 9800")
        return False

def returnSettFile():
    defaultPort = 9800
    x = checkSettFile()
    if x is True:
        with open('NetworkSettings.dat', 'rb') as f:
            #Load the data from the save file
            filePort = pickle.load(f)
            f.close()
        return filePort
    else:
        return defaultPort

def writeSettFile():
    filePort = input("Please input a port for the server to use:")
    try:
        filePort = int(filePort)
    except:
        print("Input must be a whole number.")
        return
    with open('NetworkSettings.dat', 'wb') as f:
        pickle.dump(filePort, f)
        #print("Port saved to file.")
        f.close()
        return

def silentWriteSettFile(filePort):
    try:
        filePort = int(filePort)
    except:
        filePort = 9800
    with open('NetworkSettings.dat', 'wb') as f:
        pickle.dump(filePort, f)
        #print("Port saved to file.")
        f.close()


def readFile():
    x = checkSettFile()
    if x is True:
        with open('NetworkSettings.dat', 'rb') as f:
            #Load the data from the save file
            filePort = pickle.load(f)
            f.close()
        print(f"The system is set to use port: {filePort}")
    else:
        print("[SYSTEM] File not found.")

def eraseFunc():
    if os.path.exists('NetworkSettings.dat'):
        os.remove('NetworkSettings.dat')
        print("Network settings file deleted.")
    else:
        print("[ERROR] File not found")

if __name__ == "__main__":
    print("=========================")
    print("   paNetSet v0.0.0")
    print("=========================")
    while True:
        x = input("Enter command:")
        match x:
            case "write":
                writeSettFile()
            case "read":
                readFile()
            case "erase":
                eraseFunc()
            case "exit":
                exit()
            case _:
                print("Commands are:")
                print("write = Write a new port for the system to use.")
                print("read = Check what port is being used.")
                print("erase = Erase the settings file from this directory.")
                print("exit = close the program")