import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import socket

SERVER =  "127.0.0.1"
PORT = 5000
ADDRESS = (SERVER, PORT)
HEADER_SIZE = 1024
FORMAT = 'utf-8'

class ListApp:
    def __init__(self, root):
        self.root = root
        self.root.title("List App")

        self.button_refresh = tk.Button(root, text="Refresh List", command=self.refresh_list)
        self.button_refresh.pack()

        self.button_kill = tk.Button(root, text="Kill Process", command=self.kill_process)
        self.button_kill.pack()

        self.button_start = tk.Button(root, text="Start Process", command=self.start_process)
        self.button_start.pack()

        self.button_clear = tk.Button(root, text="Clear List", command=self.clear_list)
        self.button_clear.pack()

        self.list_view = ttk.Treeview(root, columns=("Name", "ID", "Count"), show="headings")
        self.list_view.heading("Name", text="Name")
        self.list_view.heading("ID", text="ID")
        self.list_view.heading("Count", text="Count")
        self.list_view.pack()


    def refresh_list(self):
        self.list_view.delete(*self.list_view.get_children())
        
        temp = "XEM"
        self.client.send(temp.encode(FORMAT))
        temp = self.client.recv(HEADER_SIZE).decode(FORMAT)
        soprocess = int(temp)

        for _ in range(soprocess):
            s1 = self.client.recv(HEADER_SIZE).decode(FORMAT)
            if s1 == "ok":
                s1 = self.client.recv(HEADER_SIZE).decode(FORMAT)
                s2 = self.client.recv(HEADER_SIZE).decode(FORMAT)
                s3 = self.client.recv(HEADER_SIZE).decode(FORMAT)
                self.list_view.insert("", "end", values=(s1, s2, s3))

    def kill_process(self):
        temp = "KILL"
        self.client.send(temp.encode(FORMAT))
        temp = self.client.recv(HEADER_SIZE).decode(FORMAT)
        if temp == "ok":
            kill_dialog = Kill(self.root)
            kill_dialog.wait_window()

    def start_process(self):
        temp = "START"
        self.client.send(temp.encode(FORMAT))
        temp = self.client.recv(HEADER_SIZE).decode(FORMAT)
        if temp == "ok":
            start_dialog = Start(self.root)
            start_dialog.wait_window()

    def clear_list(self):
        self.list_view.delete(*self.list_view.get_children())

    def list_app_closing(self):
        temp = "QUIT"
        self.client.send(temp.encode(FORMAT))
        self.client.close()
        self.root.destroy()

class Kill(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Kill Process")

        self.label = tk.Label(self, text="Kill Process Dialog")
        self.label.pack()

        self.button_ok = tk.Button(self, text="OK", command=self.ok)
        self.button_ok.pack()

    def ok(self):
        self.destroy()

class Start(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Start Process")

        self.label = tk.Label(self, text="Start Process Dialog")
        self.label.pack()

        self.button_ok = tk.Button(self, text="OK", command=self.ok)
        self.button_ok.pack()

    def ok(self):
        self.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = ListApp(root)
    root.mainloop()
