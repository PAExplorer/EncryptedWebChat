import socket, select, threading, pickle, os
from PASearches import *
from makeNetSet import *
from makeServerPassword import *

port = 9800
port = returnSettFile()

CONFIRMMESSAGE = b"SERVER: Your credentials have been accepted"
global socketList
global blacklist
socketList = [] #users connected but do not have password credentials "Waiting room"
blacklist = [] #ip addresses to automatically reject

#Prepare the server socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind(('', port))

maxAttempts = 5

def handleClient(conn, addr):
    print(f"New user {addr} attempting to connect.")
    connected = True
    credentials = False
    attempts = 5
    print("SERVER: New connection, awaiting password for this server.")
    while connected:
        ready = select.select([conn], [], [], 0)
        if ready:
            try:
                message = conn.recv(1024)
                if message:
                    print(f"Recieved data from {addr}")
                    if message and credentials == True:
                        #Connected and has good password handle messages here
                        sendToConnected(message)
                    elif message and credentials == False:
                        #Connected but awaiting correct password
                        if message.startswith(b"#") and checkPass(message[1:]) == True:
                            credentials = True
                            #add this socket to the users who will recieve messages
                            addToSockets(conn)
                            conn.send(CONFIRMMESSAGE) #ABC
                        elif message.startswith(b"#") and checkPass(message[1:]) == False:
                            attempts -= 1
                            print(f"SERVER: Incorrect password, user has {attempts} attempts left.")
                            conn.send(b"Wrong password")
                        else:
                            attempts -= 1
                            print(f"SERVER: Bad format password or other error, user has {attempts} attempts left.")
                            conn.send(b"Wrong password")
                        if attempts <= 0:
                            connected = False
                            print(f"SERVER: User with ip address {addr[0]} has failed too many password attempts and will be blacklisted.")
                            addToBlacklist(addr[0])
            except ConnectionResetError:
                print("Error listening to client")
                connected = False
    conn.close()

def start():
    server_socket.listen()
    print(f"[SYSTEM] Server is configured using port {port}")
    print(f"[SYSTEM] Server is listening...")
    while True:
        conn, addr = server_socket.accept()
        print(addr)
        if linSearch(blacklist, addr[0]) != True:
            thread = threading.Thread(target=handleClient, args=(conn, addr))
            thread.start()
            print(f"[SYSTEM] Active connections: {threading.active_count() - 1}")

def sendToConnected(data):
    for i in range(len(socketList)):
        #if i != 0: #exclude the server itself
        #print("Sending to socket: " + str(i) + " : " + str(socketList[i]))
        try:
            socketList[i].sendall(data) #This needs a way to time out
        except:
            continue

def addToBlacklist(ip): #Save this as a local file
    blacklist.append(ip)
    with open('blacklist.dat', 'wb') as f:
        pickle.dump(blacklist, f)
        f.close()

def loadBlacklist():
    with open('blacklist.dat', 'rb') as f:
        #Load the data from the user file
        blacklist = pickle.load(f)
        f.close()
    return blacklist

def addToSockets(sock):
    socketList.append(sock)

print("Server starting...")

if os.path.exists('blacklist.dat'):
    blacklist = loadBlacklist()
    print("Blacklist successfully loaded...")
else:
    print("No blacklist found, assuming empty list.")

start()