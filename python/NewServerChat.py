import socket, select, threading

port = 9800
global socket_list
global blacklist
socketList = [] #users connected but do not have password credentials "Waiting room"
blacklist = [] #ip addresses to automatically reject

#Prepare the server socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind(('', port))

#Server specific variables
bsPassword = b"#123abc" #The password that tells the server to confirm that this socket should recieve the broadcasted messages.
maxAttempts = 5

#It may be useful to move these to their own script so that they may be improved upon seperately if you wish to do so
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