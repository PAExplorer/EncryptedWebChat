import socket, select

client_socket = socket.socket()
port = 9800
client_socket.connect(('127.0.0.1',port))
timeout_time = 10 #timeout in seconds
running = True

#recieve connection message from server
recv_msg = client_socket.recv(1024) #what is this?
print(recv_msg)

#send user details to server, this will then need to be a password system
send_msg = input("Enter your user name(prefix with #):") #get string input from user as a username
send_msg = bytes(send_msg, 'utf-8') #convert the string to a utf-8 encoding bytes
client_socket.sendall(send_msg) #to the server then send the username
client_socket.setblocking(0)


#recieve and send message from/to different users
while True:
    
    if send_msg == 'exit':
        break
    else:
        send_msg = bytes(send_msg, 'utf-8') #since we're not exiting, encode the string then send it.
        client_socket.sendall(send_msg)

client_socket.close()

def primaryRecieve():
    ready = select.select([client_socket], [], [], timeout_time) #check if message is ready
    send_msg = input(b"Send your message in format [@user:message] ") #This will need to be a function later but we'll build a GUI first anyway
    if ready[0]: #if our ready flag is triggered then go ahead and recieve the thing
        recv_msg = client_socket.recv(1024) #When the message is ready, go ahead and recieve
        print(recv_msg)

def primarySend():
    print("sendy")
