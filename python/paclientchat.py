import socket, select, time

client_socket = socket.socket()
port = 9800
timeout_time = 10 #timeout in seconds
client_socket.setblocking(0)


def connectSocket(ip='127.0.0.1'):
    try:
        client_socket.connect((ip,port))
    except:
        time.sleep(1)
    else:
        print("User connected")

def encryptString():
    print("Mr.encryption")

def primaryRecieve():
    ready = select.select([client_socket], [], [], timeout_time) #check if message is ready
    if ready[0]: #if our ready flag is triggered then go ahead and recieve the thing
        recv_msg = client_socket.recv(1024) #When the message is ready, go ahead and recieve
        return str(recv_msg, 'utf-8')
    else:
        return "0"

def primarySend(send_msg):
    send_msg = bytes(send_msg, 'utf-8')
    client_socket.sendall(send_msg)

def closeConnection():
    client_socket.close()

connectSocket()