import socket, select, errno, os

#This is a segment of code for password authentication that will allow us to reject or accept users in the chat lobby
#We need to limit the number of attempts that can be made to 5


port = 9800
socket_list = [] #users connected but do not have password credentials "Waiting room"
connected_socket_list =[] #users who connected and and have given the correct password. "In the club" get transmitted messages.
users = {}
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind(('', port))
server_socket.listen(5) #Listen to the socket, tries 5 times, this will need to be changed to use "Select"
server_socket.setblocking(0) #set the socket to non blocking so that the function will never hang indefinitely
socket_list.append(server_socket)
bsPassword = b"#123abc"
TIMEOUT = 1
nAttempts = [0]
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

#EXECUTION
print("Server started")
while True:
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