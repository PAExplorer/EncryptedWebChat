import socket, select, errno, os
from sqlite3 import Time

port = 9800
socket_list = []
users = {}
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind(('', port))
server_socket.listen(5) #Listen to the socket, tries 5 times, this will need to be changed to use "Select"
socket_list.append(server_socket)
TIMEOUT = 1

class TimeoutError(Exception):
    pass

def handleTimeout(signum, frame):
    raise TimeoutError(os.strerror(errno.ETIME))

def linSearch(list, product):
    for i in range(len(list)):
        if list[i] == product:
            return True
    return False


print("Chat Server Started")

while True:
    ready_to_read,ready_to_write,in_error = select.select(socket_list,[],[],0)
    for sock in ready_to_read:
        if sock == server_socket:
            connect, addr = server_socket.accept()
            if linSearch(socket_list, connect) != True:
                print("New connection added...")
                socket_list.append(connect)
                BSAddr = bytes(str(addr), 'utf-8') #Funky thing to convert the ip address to a string then encode it to bytestring
                connect.sendall(b"You are connected from:" + BSAddr)
        else:
            try:
                data = sock.recv(1024)
                strData = str(data, 'utf-8')
                print("====================")
                print("Recieved data: " + strData)
                print("====================")
                if strData.startswith("#"):
                    users[data[1:].lower()]=connect

                    print("User " + strData[1:] + " added.")

                    print("Connection Data: " + str(connect))
                    print("Users: " + str(users))

                    sendName = bytes("\nYour user detail saved as : " + strData[1:], 'utf-8') #get that username and convert it to bytes for sending back

                    connect.sendall(sendName)
                    print("Connection response complete.")

                if strData.startswith("@"):
                    print("Recieved incoming message successfully")
                    for i in range(len(socket_list)):
                        if i != 0: #exclude the server itself
                            print("Sending to socket: " + str(i) + " : " + str(socket_list[i]))
                            try:
                                socket_list[i].sendall(data[1:]) #This needs a way to time out
                            except:
                                continue
            except:
                continue

server_socket.close()