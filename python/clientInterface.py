import tkinter as tk
import tkinter.ttk as ttk
from tkinter import font

events=[]
#define our GUI elements we are going to use for this window interface
frameA = tk.Frame(background='#2e2e2e')
frameB = tk.Frame(background='#2e2e2e')
frameC = tk.Frame(background='#2e2e2e')

def handleButtonPress(event=None):
    sText = entry.get()
    addToChatWindow(sText)
    entry.delete(0, tk.END)

def addToChatWindow(sChat):
    sChat = "\n" + sChat
    chatTextBox.configure(state="normal")
    chatTextBox.insert(tk.END, sChat)
    chatTextBox.configure(state="disabled")

def openSettings(event=None):
    settingsWindow = settingsWin(window)
    settingsWindow.grab_set()

label = ttk.Label(
    text="Hello, tkinter",
    foreground='#dbdbce',
    background='#2e2e2e',
    font=("Roboto", 16, font.BOLD),
    master=frameA
)

button = tk.Button(
    text = "Send",
    width=10,
    master=frameB,
    command=handleButtonPress
)
settingsButton = tk.Button(
    text = "Settings",
    width=10,
    master=frameC,
    command=openSettings
)

entry = tk.Entry(
    foreground='#dbdbce',
    background='#2e2e2e',
    font=("Roboto", 14),
    master=frameB
)

chatTextBox = tk.Text(
    font=("Roboto", 14),
    background='#2e2e2e',
    foreground='#dbdbce',
    master=frameA
)


border_effects = {

    "flat": tk.FLAT,

    "sunken": tk.SUNKEN,

    "raised": tk.RAISED,

    "groove": tk.GROOVE,

    "ridge": tk.RIDGE,
    
    #Usage: 
}

class window(tk.Tk):
    def __init__(self):
        super().__init__()
        self.geometry("600x800")
        self.configure(background='#2e2e2e')
        self.title('Main Window')

class settingsWin():
    def __init__(self, window):
        super().__init__(window)
        self.geometry("600x300")
        self.title('Settings')
        self.configure(background='#2e2e2e')

        #subwidgets go here
        tk.Button(self, text='Close', command=self.destroy).pack(expand=True)

label.pack(padx=15, pady=5)
chatTextBox.pack(fill='both', expand=tk.TRUE, padx=15, pady=15)
entry.pack(fill=tk.BOTH, expand=tk.TRUE, side=tk.LEFT, padx=15, pady=15)
button.pack(side=tk.RIGHT, padx=15, pady=15)
frameA.pack(fill='both', expand=tk.TRUE)
frameB.pack(fill='x')
settingsButton.pack()
frameC.pack()

chatTextBox.configure(state="disabled")

entry.bind('<Return>', handleButtonPress)

#entryInput = entry.get()
#entry.delete(0) or entry.delete(0,4) of entry.delete(0, tk.END) #This deletes the defined char inside the entry cell
#entry.intert("Inserted Text goes here")
#chatTextBox.get("1.0", "2.5") line 1 element 0 to line 2 element 5 you may also use tk.END 
#chatTextBox.delete("1.0") works like the above with ranges as well
#chatTextBox.insert(tk.End, "\nThe string you want added")

window.mainloop()
