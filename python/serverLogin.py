import socket, select, threading

#This is a segment of code for password authentication that will allow us to reject or accept users in the chat lobby
#We need to limit the number of attempts that can be made to 5


port = 9800
#ip = socket.gethostbyname(socket.gethostbyname())
global socket_list
global blacklist
socket_list = [] #users connected but do not have password credentials "Waiting room"
blacklist = [] #ip addresses to automatically reject

#Prep server socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind(('', port))

#server_socket.listen(5) #Listen to the socket, tries 5 times, this will need to be changed to use "Select"
#server_socket.setblocking(0) #set the socket to non blocking so that the function will never hang indefinitely
#socket_list.append(server_socket)

#Server specific variables
bsPassword = b"#123abc" #The password that tells the server to confirm that this socket should recieve the broadcasted messages.
maxAttempts = 5

def linSearch(list, product):
    for i in range(len(list)):
        if list[i] == product:
            return True
    return False

def giveLinSearch(list, product):
    for i in range(len(list)):
        if list[i] == product:
            return i
    return -1

def handleClient(conn, addr):
    print(f"New user {addr} attempting to connect.")
    connected = True
    credentials = False
    attempts = 5
    conn.send(b"SERVER: New connection, please provide the password for this server.")
    while connected:
        ready = select.select([conn], [], [], 0)
        if ready:
            message = conn.recv(1024)
            print("Recieved data: " + str(message, 'utf-8'))
            if message and credentials == True:
                #Connected and has good password handle messages here
                sendToConnected(message)
            elif message and credentials == False:
                #Connected but awaiting correct password
                if message.startswith(b"#") and message == bsPassword:
                    credentials = True
                    #add this socket to the users who will recieve messages
                    addToSockets(conn)
                    conn.send(b"SERVER: Your credentials have been accepted")
                elif message.startswith(b"#") and message != bsPassword:
                    attempts -= 1
                    conn.send(b"SERVER: Incorrect password, you have some attempts left.")
                else:
                    attempts -= 1
                    conn.send(b"SERVER: Bad format password or other error, you have some attempts left.")
                if attempts <= 0:
                    connected = False
                    addToBlacklist(addr[0])
    conn.close()





def start():
    server_socket.listen()
    print(f"[LISTENING] Server is listening")
    while True:
        conn, addr = server_socket.accept()
        print(addr)
        if linSearch(blacklist, addr[0]) != True:
            thread = threading.Thread(target=handleClient, args=(conn, addr))
            thread.start()
            print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 1}")

def sendToConnected(data):
    for i in range(len(socket_list)):
        #if i != 0: #exclude the server itself
        print("Sending to socket: " + str(i) + " : " + str(socket_list[i]))
        try:
            socket_list[i].sendall(data) #This needs a way to time out
        except:
            continue

def addToBlacklist(ip): #Save this as a local file
    blacklist.append(ip)

def addToSockets(sock):
    socket_list.append(sock)


#EXECUTION
print("Server starting...")
start()

while False:
    ready_to_read,ready_to_write,in_error = select.select(socket_list,[],[],0)
    for sock in ready_to_read:
            if sock == server_socket:
                connect, addr = server_socket.accept()
                if linSearch(socket_list, connect) != True:
                    print("Recieved new connection request...")
                    socket_list.append(connect) #add socket to waiting room
                    nAttempts.append(maxAttempts) #add equivalent counter for that socket
                    BSAddr = bytes(str(addr), 'utf-8')
                    connect.sendall(b"You are connected from:" + BSAddr)
            else:
                try:
                    data = sock.recv(1024)
                    strData = str(data, 'utf-8')
                    if strData.startswith("#") and data == bsPassword:
                        print("Received GOOD password")
                        connect.sendall(b"Password accepted")
                        connected_socket_list.append(connect)
                        if giveLinSearch(socket_list, connect) != -1: #not null entry
                            i = giveLinSearch(socket_list, connect)
                            socket_list.pop(i) #remove from "Waiting room"
                            nAttempts.pop(i)
                        print("Report")
                        print("=====Connected Users:=====")
                        print(connected_socket_list)
                        print("=========================")
                        print("=====Waiting Room:=====")
                        print(socket_list)
                        print("=========================")
                        print("=====Number of attempts left:=====")
                        print(nAttempts)
                        print("=========================")
                        exit()
                    elif strData.startswith("#") and data != bsPassword:
                        print("Received BAD password")
                        if giveLinSearch(socket_list, connect) != -1: #not null entry
                            print("Succesfully found attempted socket connector, decrementing counter")
                            i = giveLinSearch(socket_list, connect)
                            print(i)
                            x = nAttempts[i]
                            nAttempts[i] = x - 1
                            print(nAttempts[i])
                            print("===== Begining of Report =====")
                            print("=====Connected Users:=====")
                            print(connected_socket_list)
                            print("=========================")
                            print("=====Waiting Room:=====")
                            print(socket_list)
                            print("=========================")
                            print("=====Number of attempts left:=====")
                            print(nAttempts)
                            print("=========================")
                            print("===== END OF REPORT ======")
                            if nAttempts[i] < 0:
                                print("USER BLACKLISTED!!")
                                #Add the socket to the blacklist here
                        connect.sendall(b"Password rejected. you have " + x + " remaining attempts.")
                except:
                    continue