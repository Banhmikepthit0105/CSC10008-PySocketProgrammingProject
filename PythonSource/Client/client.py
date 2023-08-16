# import tkinter as tk
# from tkinter import messagebox
# import socket
# from GUI.handle_listAppGUI import ListApp
# from GUI.handle_picsGUI import Pic 
# from GUI.handle_keylogGUI import Keylog 
# from GUI.handle_processGUI import Process  

# class ClientApp(tk.Tk):
#     def __init__(self):
#         super().__init__()

#         self.title("Client")
#         self.geometry("300x250")

#         self.butConnect = tk.Button(self, text="Connect", command=self.connect_to_server)
#         self.butConnect.pack()

#         self.butApp = tk.Button(self, text="List Applications", command=self.open_applications)
#         self.butApp.pack()

#         self.butReg = tk.Button(self, text="Registry", command=self.open_registry)
#         self.butReg.pack()

#         self.butPic = tk.Button(self, text="Take Picture", command=self.take_picture)
#         self.butPic.pack()

#         self.butKeyLog = tk.Button(self, text="Keylogger", command=self.open_keylogger)
#         self.butKeyLog.pack()

#         self.butProcess = tk.Button(self, text="Processes", command=self.open_processes)
#         self.butProcess.pack()

#         self.butShutdown = tk.Button(self, text="Shutdown", command=self.shutdown)
#         self.butShutdown.pack()

#         self.butExit = tk.Button(self, text="Exit", command=self.exit_client)
#         self.butExit.pack()

#         self.client = None
#         self.nw = None
#         self.nr = None

#         self.protocol("WM_DELETE_WINDOW", self.client_closing)

#     def connect_to_server(self):
#         if self.client:
#             messagebox.showinfo("Info", "Already connected to server.")
#             return

#         try:
#             server_ip = self.txtIP.get()
#             server_port = 5656
#             self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#             self.client.connect((server_ip, server_port))
#             self.nw = self.client.makefile(mode="w")
#             self.nr = self.client.makefile(mode="r")
#             messagebox.showinfo("Info", "Connected to server successfully.")
#         except Exception as e:
#             messagebox.showerror("Error", "Failed to connect to server: " + str(e))
#             self.client = None

#     def open_applications(self):
#         if not self.client:
#             messagebox.showinfo("Info", "Not connected to server.")
#             return

#         self.nw.write("APPLICATION\n")
#         self.nw.flush()
#         viewApp = ListApp(self.nw, self.nr)
#         viewApp.wait_window()


#     def take_picture(self):
#         if not self.client:
#             messagebox.showinfo("Info", "Not connected to server.")
#             return

#         self.nw.write("TAKEPIC\n")
#         self.nw.flush()
#         viewPic = Pic(self.nw, self.nr)
#         viewPic.lam()
#         viewPic.wait_window()

#     def open_keylogger(self):
#         if not self.client:
#             messagebox.showinfo("Info", "Not connected to server.")
#             return

#         self.nw.write("KEYLOG\n")
#         self.nw.flush()
#         viewKeylog = Keylog(self.nw, self.nr)
#         viewKeylog.wait_window()

#     def open_processes(self):
#         if not self.client:
#             messagebox.showinfo("Info", "Not connected to server.")
#             return

#         self.nw.write("PROCESS\n")
#         self.nw.flush()
#         viewProcess = Process(self.nw, self.nr)
#         viewProcess.wait_window()

#     def shutdown(self):
#         if not self.client:
#             messagebox.showinfo("Info", "Not connected to server.")
#             return

#         self.nw.write("SHUTDOWN\n")
#         self.nw.flush()
#         self.client.close()
#         self.client = None

#     def exit_client(self):
#         if self.client:
#             self.nw.write("QUIT\n")
#             self.nw.flush()
#             self.client.close()

#         self.destroy()

#     def client_closing(self):
#         if self.client:
#             self.nw.write("QUIT\n")
#             self.nw.flush()
#             self.client.close()

#         self.destroy()

# if __name__ == "__main__":
#     app = ClientApp()
#     app.mainloop()







import socket
from GUI import handle_clientGUI
from GUI import handle_keylogGUI
from GUI import handle_listAppGUI
from GUI import handle_picsGUI
from GUI import handle_processGUI
from GUI import handle_startGUI
from GUI import communicate


SERVER =  "127.0.0.1"
PORT = 5000
ADDRESS = (SERVER, PORT)
HEADER_SIZE = 1024
DISCONNECT_MESSAGE = "!DISCONNECT"
FORMAT = "utf-8"


client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = (ADDRESS)
print("Client connect to server with port: " + str(PORT))
client.connect(ADDRESS)

try: 
    while True:
        message = input('Client: ')
        client.sendall(bytes(message, FORMAT))
        # if (message == "Process Running"):

        respond = client.recv(HEADER_SIZE)
        tmpRes = respond.decode(FORMAT)
        command = message
        if (command == "Process Running"):
            handle_processGUI.mainProcess()
        if (command == "App Running"):
            handle_listAppGUI.mainListApp()
        if (command == "Taking Screenshot"): 
            handle_picsGUI.mainPics()
        if (command == "Keystroke"):
            handle_keylogGUI.mainKeylogger()
        if (command == "Start"):
            handle_startGUI.mainStart()

        print("Server has accepted: ", respond.decode(FORMAT))
except KeyboardInterrupt:
    client.close()
finally:
    client.close()



# def sendMessage(msg):
#     message = msg.encode(FORMAT)
#     message_length = len(message)
#     send_length = str(message_length).encode(FORMAT)
#     send_length += b' ' * (HEADER_SIZE - len(send_length))
#     client.send(send_length)
#     client.send(message)

# sendMessage("Hello World")
# sendMessage("Hello Thai")
# sendMessage("Hello WORLDD")
# sendMessage("Hellooooo")
# sendMessage("Hellooooo")
# sendMessage(DISCONNECT_MESSAGE)