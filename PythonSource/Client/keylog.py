import tkinter as tk
import socket

SERVER =  "127.0.0.1"
PORT = 5000
ADDRESS = (SERVER, PORT)
HEADER_SIZE = 1024
FORMAT = 'utf-8'

class KeylogApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Keylog App")

        self.button_hook = tk.Button(root, text="Hook", command=self.hook)
        self.button_hook.pack()

        self.button_unhook = tk.Button(root, text="Unhook", command=self.unhook)
        self.button_unhook.pack()

        self.button_print = tk.Button(root, text="Print", command=self.print_keylog)
        self.button_print.pack()

        self.txt_kq = tk.Text(root, height=10, width=40)
        self.txt_kq.pack()

        self.button_clear = tk.Button(root, text="Clear", command=self.clear)
        self.button_clear.pack()

        self.root.protocol("WM_DELETE_WINDOW", self.keylog_app_closing)

        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect(ADDRESS)

    def hook(self):
        s = "HOOK"
        self.client.send(s.encode(FORMAT))

    def unhook(self):
        s = "UNHOOK"
        self.client.send(s.encode(FORMAT))

    def print_keylog(self):
        s = "PRINT"
        self.client.send(s.encode(FORMAT))
        data = self.client.recv(HEADER_SIZE).decode(FORMAT)
        self.txt_kq.insert(tk.END, data)

    def clear(self):
        self.txt_kq.delete(1.0, tk.END)

    def keylog_app_closing(self):
        s = "QUIT"
        self.client.send(s.encode(FORMAT))
        self.client.close()
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = KeylogApp(root)
    root.mainloop()
