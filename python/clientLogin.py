import select, socket

client_socket = socket.socket()
port = 9800
timeout_time = 10 #timeout in seconds

#client_socket.setblocking(0)
backgroundColor = '#2e2e2e'
foregroundColor = '#dbdbce'
serverIp = '127.0.0.1'
passKey = '123abc'
quitFlag = True

if __name__ == "__main__":
    client_socket.connect((serverIp,port))
    recv_msg = client_socket.recv(1024)
    print(recv_msg)
    messageToSend = bytes(input(), 'utf-8')
    for i in range(0,10):
        try:
            client_socket.sendall(messageToSend)
        except:
            print("error sending data")
        print("Data Sent")
        recv_msg = client_socket.recv(1024)
        print(recv_msg)
