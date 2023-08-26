import tkinter as tk
from tkinter import messagebox
import socket

SERVER =  "127.0.0.1"
PORT = 5000
ADDRESS = (SERVER, PORT)
HEADER_SIZE = 1024
FORMAT = 'utf-8'

class StartApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Start App")

        self.label = tk.Label(root, text="Enter Process ID:")
        self.label.pack()

        self.txt_id = tk.Entry(root)
        self.txt_id.pack()

        self.but_start = tk.Button(root, text="Start Process", command=self.start_process)
        self.but_start.pack()

        self.root.protocol("WM_DELETE_WINDOW", self.start_app_closing)

        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect(ADDRESS)

    def start_process(self):
        process_id = self.txt_id.get()

        self.client.send("START ID".encode(FORMAT))
        self.client.send(process_id.encode(FORMAT))
        
        response = self.client.recv(HEADER_SIZE).decode(FORMAT)
        messagebox.showinfo("Start Process", response)

    def start_app_closing(self):
        self.client.send("QUIT".encode(FORMAT))
        self.client.close()
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = StartApp(root)
    root.mainloop()
