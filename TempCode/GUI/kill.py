import tkinter as tk
from tkinter import messagebox
import socket


SERVER =  "127.0.0.1"
PORT = 5000
ADDRESS = (SERVER, PORT)
HEADER_SIZE = 1024
FORMAT = 'utf-8'

class KillApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Kill App")

        self.label = tk.Label(root, text="Enter Process ID:")
        self.label.pack()

        self.txt_id = tk.Entry(root)
        self.txt_id.pack()

        self.but_nhap = tk.Button(root, text="Kill Process", command=self.kill_process)
        self.but_nhap.pack()

        self.root.protocol("WM_DELETE_WINDOW", self.kill_app_closing)

        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect(ADDRESS)

    def kill_process(self):
        process_id = self.txt_id.get()

        self.client.send("KILLID".encode(FORMAT))
        self.client.send(process_id.encode(FORMAT))
        
        response = self.client.recv(HEADER_SIZE).decode(FORMAT)
        messagebox.showinfo("Kill Process", response)

    def kill_app_closing(self):
        self.client.send("QUIT".encode())
        self.client.close()
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = KillApp(root)
    root.mainloop()
