#---------TESTING THE COMUNICATION BETWEEN CLIENT AND SERVER--------------------------


# import socket

# SERVER =  "127.0.0.1"
# PORT = 5000
# ADDRESS = (SERVER, PORT)
# HEADER_SIZE = 1024
# DISCONNECT_MESSAGE = "!DISCONNECT"
# FORMAT = "utf-8"


# client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# server_address = (ADDRESS)
# # print("Client connect to server with port: " + str(PORT))
# client.connect(ADDRESS)

# # try: 
# #     while True:
# #         msg = input('Client: ')
# #         client.sendall(bytes(msg, FORMAT))
# # except KeyboardInterrupt:
# #     client.close()
# # finally:
# #     client.close()


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


#------------MAIN CLIENT APPLICATION----------------------
import tkinter as tk
import socket
import threading

class ClientApp:
    def __init__(self):
        self.client = None

        self.root = tk.Tk()
        self.root.title("Client")

        self.butApp = tk.Button(self.root, text="App Running", command=self.butApp_Click)
        self.butApp.pack()

        self.butConnect = tk.Button(self.root, text="Kết nối", command=self.butConnect_Click)
        self.butConnect.pack()

        self.txtIP = tk.Entry(self.root)
        self.txtIP.insert(0, "Nhập IP")
        self.txtIP.pack()

        self.butTat = tk.Button(self.root, text="Tắt máy", command=self.butTat_Click)
        self.butTat.pack()

        self.butReg = tk.Button(self.root, text="Sửa registry", command=self.butReg_Click)
        self.butReg.pack()

        self.butExit = tk.Button(self.root, text="Thoát", command=self.butExit_Click)
        self.butExit.pack()

        self.butPic = tk.Button(self.root, text="Chụp màn hình", command=self.butPic_Click)
        self.butPic.pack()

        self.butKeyLock = tk.Button(self.root, text="Keystroke", command=self.butKeyLock_Click)
        self.butKeyLock.pack()

        self.butProcess = tk.Button(self.root, text="Process Running", command=self.butProcess_Click)
        self.butProcess.pack()

        self.root.protocol("WM_DELETE_WINDOW", self.client_Closing)

    def start(self):
        self.root.mainloop()

    def butApp_Click(self):
        if self.client is None:
            self.show_message("Chưa kết nối đến server")
            return

        s = "APPLICATION"
        self.send_message(s)
        self.show_message("App Running")
        # Add code to handle the response and open the corresponding dialog

    def butConnect_Click(self):
        ip = self.txtIP.get()
        if not ip:
            self.show_message("Vui lòng nhập IP")
            return

        try:
            self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.client.connect((ip, 5656))
            self.show_message("Kết nối đến server thành công")
            self.start_receiver_thread()
        except Exception as ex:
            self.show_message("Lỗi kết nối đến server")

    def start_receiver_thread(self):
        threading.Thread(target=self.receive_thread).start()

    def receive_thread(self):
        while self.client:
            try:
                data = self.client.recv(1024).decode()
                if not data:
                    break
                # Process received data
            except:
                break
        self.client = None

    def send_message(self, message):
        if self.client:
            self.client.sendall(message.encode())

    def butTat_Click(self):
        if self.client is None:
            self.show_message("Chưa kết nối đến server")
            return

        s = "SHUTDOWN"
        self.send_message(s)
        self.client.close()
        self.client = None

    def butReg_Click(self):
        if self.client is None:
            self.show_message("Chưa kết nối đến server")
            return

        s = "REGISTRY"
        self.send_message(s)
        self.show_message("Sửa registry")
        # Add code to handle the response and open the corresponding dialog

    def butExit_Click(self):
        s = "QUIT"
        self.send_message(s)
        self.root.destroy()

    def butPic_Click(self):
        if self.client is None:
            self.show_message("Chưa kết nối đến server")
            return

        s = "TAKEPIC"
        self.send_message(s)
        # Add code to handle the response and open the corresponding dialog

    def butKeyLock_Click(self):
        if self.client is None:
            self.show_message("Chưa kết nối đến server")
            return

        s = "KEYLOG"
        self.send_message(s)
        # Add code to handle the response and open the corresponding dialog

    def butProcess_Click(self):
        if self.client is None:
            self.show_message("Chưa kết nối đến server")
            return

        s = "PROCESS"
        self.send_message(s)
        # Add code to handle the response and open the corresponding dialog

    def client_Closing(self):
        if self.client:
            self.send_message("QUIT")
            self.client.close()
            self.client = None
        self.root.destroy()

    def show_message(self, message):
        tk.messagebox.showinfo("Thông báo", message)

if __name__ == "__main__":
    app = ClientApp()
    app.start()
