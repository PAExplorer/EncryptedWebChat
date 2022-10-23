import tkinter as tk
import tkinter.ttk as ttk
from tkinter import font
import select, socket, pickle, threading, multiprocessing

defaultFont = "Segoe UI Emoji"
selfUser = "Me:"
client_socket = socket.socket()
port = 9800
timeout_time = 10 #timeout in seconds

#client_socket.setblocking(0)
backgroundColor = '#2e2e2e'
foregroundColor = '#dbdbce'
serverIp = '127.0.0.1'
encKey = '123abc'

class settingsWin(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.geometry("600x300")
        self.title('Settings')
        self.configure(background=backgroundColor)

        #create subwidgets
        self.nameLabel = ttk.Label(
            self,
            text="Username:",
            foreground=foregroundColor,
            background=backgroundColor,
            font=(defaultFont, 10)  
        ).pack()
        #self.nameLabel.pack()
        self.nameEntry = tk.Entry(self)
        self.nameEntry.pack(expand=True)
        self.nameEntry.insert(0, loadSettings(0))
        self.ipLabel = ttk.Label(
            self,
            text="Server ip:",
            foreground=foregroundColor,
            background=backgroundColor,
            font=(defaultFont, 10)  
        ).pack()
        self.ipEntry = tk.Entry(self)
        self.ipEntry.pack(expand=True)
        self.ipEntry.insert(0, loadSettings(1))
        self.keyLabel = ttk.Label(
            self,
            text="Encryption key:",
            foreground=foregroundColor,
            background=backgroundColor,
            font=(defaultFont, 10)  
        ).pack()
        self.keyEntry = tk.Entry(self)
        self.keyEntry.pack(expand=True)
        self.keyEntry.insert(0, loadSettings(2))
        self.exitBut = tk.Button(self, text='Save and Close', command=self.saveVars).pack(expand=True)
    def saveVars(self,):
        saveSettings(self.nameEntry.get(), self.ipEntry.get(), self.keyEntry.get())
        self.destroy()

class window(tk.Tk):
    def __init__(self):
        super().__init__()
        self.geometry("600x800")
        self.configure(background=backgroundColor)
        self.title('Main Window')

        self.events=[]
        #define our GUI elements we are going to use for this window interface
        self.frameA = tk.Frame(background=backgroundColor)
        self.frameB = tk.Frame(background=backgroundColor)
        self.frameC = tk.Frame(background=backgroundColor)

        self.label = ttk.Label(
            text="Mr.Cryptochat",
            foreground=foregroundColor,
            background=backgroundColor,
            font=(defaultFont, 16, font.BOLD),
            master=self.frameA    
        )
        self.setBut = tk.Button( #Button
            text='Settings',
            foreground=foregroundColor,
            background=backgroundColor,
            font=(defaultFont, 10),
            command=self.openWindow,
            master=self.frameC)

        self.sendBut = tk.Button( #Button
            text='Send',
            foreground=foregroundColor,
            background=backgroundColor,
            font=(defaultFont, 10),
            command=self.handleButtonPress,
            master=self.frameC)
        
        self.chatTextBox = tk.Text(
            font=(defaultFont, 14),
            background=backgroundColor,
            foreground=foregroundColor,
            master=self.frameA
        )
        self.entry = tk.Entry(
            foreground=foregroundColor,
            background=backgroundColor,
            font=(defaultFont, 14),
            master=self.frameC
        )

        self.label.pack(padx=15, pady=5)
        self.frameA.pack(fill='both', expand=tk.TRUE)
        self.chatTextBox.pack(fill='both', expand=tk.TRUE, padx=15, pady=5)
        self.frameB.pack(fill='x')
        self.setBut.pack(padx=15, pady=5, side=tk.RIGHT)
        self.sendBut.pack(padx=5, pady=5, side=tk.RIGHT)
        self.entry.pack(fill=tk.BOTH, expand=tk.TRUE, side=tk.LEFT, padx=15, pady=5)
        self.frameC.pack(fill='x')

        self.entry.bind('<Return>', self.handleButtonPress)
    def openWindow(self):
        setWin = settingsWin(self)
        setWin.grab_set()
    def handleButtonPress(self,event=None):
        #When committing the chat in your form send to the function that handles contacting the server. The server should send it back
        print("A")
        sText = "@" + loadSettings(0) + ": " + self.entry.get()
        primarySend(sText)
        self.entry.delete(0, tk.END)
    def addToChatWindow(self, sChat = "..."):
        inMessage = "\n" + sChat
        self.chatTextBox.configure(state="normal")
        self.chatTextBox.insert(tk.END, inMessage)
        self.chatTextBox.see(tk.END)
        self.chatTextBox.configure(state="disabled")

def connectSocket(ip='127.0.0.1'):
    try:
        client_socket.connect((ip,port))
    except socket.error:
        app.addToChatWindow("System: Error connecting to host server")

    #client_socket.sendall(bytes("#" + loadSettings(0), 'utf-8'))

def isStillConnected(sock):
    try:
        sock.sendall(b"ping")
        return True
    except:
        return False

def encryptString():
    print("Mr.encryption")

def primaryRecieve():
    ready = select.select([client_socket], [], [], timeout_time) #check if message is ready
    if ready[0]: #if our ready flag is triggered then go ahead and recieve the thing
        recv_msg = client_socket.recv(1024) #When the message is ready, go ahead and recieve
        return str(recv_msg, 'utf-8')
    else:
        return "0"

def closeConnection():
    client_socket.close()

def saveSettings(sUserName, sServerIp, sEncKey):
    global selfUser
    global serverIp
    global encKey
    selfUser = sUserName
    serverIp = sServerIp
    encKey = sEncKey
    #Then Save To Local File!
    with open('save.dat', 'wb') as f:
        pickle.dump([selfUser, serverIp, encKey], f)
        f.close()

def loadSettings(nwhichVar = 0):
    #nWhichvar is an integer which will return a certain variable from the saved file depending on what you set it to. 
    # = 0, userName
    # = 1, serverIP
    # = 2, encryption key
    with open('save.dat', 'rb') as f:
        #Load the data from the user file
        selfUser, serverIp, encKey = pickle.load(f)
        f.close()
    match nwhichVar:
        case 0:
            return selfUser
        case 1:
            return serverIp
        case 2:
            return encKey
        case _:
            #If someone is a DUMBY DUMB DUMB and asks for something out of range then return the username and hope for the best
            return selfUser

def primarySend(send_msg):
    #Check if connection is still live...
    #x = isStillConnected(client_socket)
    #If it is send the message, else throw an error into the chat
    #if x:
    print("B")
    send_msg = bytes(send_msg, 'utf-8')
    try:
        client_socket.sendall(send_msg)
    except socket.error:
        app.addToChatWindow("System: Connection Error")

app = window()

def messageListen(quitFlag):
    #Repeatedly listen to the server
    while quitFlag:
        ready = select.select([client_socket], [], [], 0) #check if message is ready
        if ready[0]: #if our ready flag is triggered then go ahead and recieve the thing
            print("Recieved Message from server...")
            recv_msg = client_socket.recv(1024) #When the message is ready, go ahead and recieve
            app.addToChatWindow(str(recv_msg, 'utf-8'))


if __name__ == "__main__":
    #Load the settings from the save file first thing
    selfUser = loadSettings(0)
    serverIp = loadSettings(1)
    encKey = loadSettings(2)
    connectSocket(serverIp)
    app.addToChatWindow("System: Connecting to server...")
    #Run the messageListen on repeat here pleas
    quitFlag = multiprocessing.Value('i', int(False))
    listenThread = threading.Thread(target=messageListen, args=(quitFlag,))
    listenThread.start()
    try:
        app.mainloop()
    except KeyboardInterrupt:
        print("Keyboard interrupt")
    quitFlag.value = True
    listenThread.join()

    