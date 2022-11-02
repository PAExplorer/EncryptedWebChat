import pickle, os, re
from PASearches import *

global blacklist
blacklist = []

regex = "^((25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])\.){3}(25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])$"


def checkBlacklist():
    if os.path.exists('blacklist.dat'):
        #print("Blacklist found")
        return True
    else:
        print("No blacklist found, assuming file does not exist.")
        return False

def loadBlacklist():
    with open('blacklist.dat', 'rb') as f:
        #Load the data from the save file
        blacklist = pickle.load(f)
        f.close()
    return blacklist

def saveBlacklist(bList):
    blacklist = bList
    with open('blacklist.dat', 'wb') as f:
        pickle.dump(blacklist, f)
        f.close()

def checkIP(Ip):
    #validate an Ip address
    if(re.search(regex, Ip)):
        print("Good IP formatting")
        return True
    else:
        print("Bad IP formatting")
        return False

def newfunc():
    x = input("This command will overwrite any existing blacklist in this directory, continue? [y/n]")
    if x == "y" or x == "Y":
        blacklist = []
        with open('blacklist.dat', 'wb') as f:
            pickle.dump(blacklist, f)
            f.close()
            print("Empty blacklist file created")
    else:
        print("[ERROR] Invalid response")

def eraseFunc():
    if os.path.exists('blacklist.dat'):
        os.remove('blacklist.dat')
        print("Blacklist file deleted")
    else:
        print("[ERROR] File not found")

def appendFunc():
    cont = True
    x = checkBlacklist()
    if x == True:
        blacklist = loadBlacklist()
        while cont:
            y = input("Ip address:")
            z = checkIP(y)
            if z == True:
                blacklist.append(y)
                kont = True
                while kont:
                    a = input("Continue appending? [y/n]")
                    if a == "y" or a == "Y":
                        print("Confirmed adding new entry")
                        kont = False
                    elif a == "n" or a == "N":
                        print("Confirmed, saving changes to file")
                        saveBlacklist(blacklist)
                        kont = False
                        cont = False
                    else:
                        print("Invalid Response")
            else:
                print("Bad ipv4 address formatting")

    else:
        print("Cannot append to file that does not exist!")

def viewFunc():
    x = checkBlacklist()
    if x == True:
        print(loadBlacklist())
    else:
        print("No blacklist found in directory")

def removeFunc():
    x = input("IP address to permit:")
    y = checkIP(x)
    z = checkBlacklist()
    if y == True and z == True:
        blacklist = loadBlacklist()
        a = giveLinSearch(blacklist, x)
        if a != -1:
            del blacklist[a]
            saveBlacklist(blacklist)
        else:
            print("[ERROR] Could not find ip address in blacklist.")
    else:
        print("[ERROR] could not delete entry")


if __name__ == "__main__":
    print("=========================")
    print("   Blacklister v0.0.0")
    print("=========================")
    checkBlacklist()
    while True:
        x = input("Enter command:")
        match x:
            case "new":
                newfunc()
            case "erase":
                eraseFunc()
            case "append":
                appendFunc()
            case "view":
                viewFunc()
            case "remove":
                removeFunc()
            case "exit":
                exit()
            case _:
                print("Commands are:")
                print("new = Create a new blacklist from scratch")
                print("erase = Erase data in existing blacklist")
                print("append = Add an entry to an existing blacklist")
                print("view = View current blacklisted ip addresses")
                print("remove = removes an entry by exact matched name, linear search")
                print("exit = exits the program")