import tkinter as tk
from tkinter import ttk

class ListAppForm:
    def __init__(self, root):
        
        self.root = root
        self.root.title("listApp")


        self.button1 = ttk.Button(root, text="Xem", command=self.on_xem_button_click)
        self.button1.pack(side=tk.LEFT, padx=10, pady=10)

        
        self.button2 = ttk.Button(root, text="Kill", command=self.on_kill_button_click)
        self.button2.pack(side=tk.LEFT, padx=10, pady=10)

        self.button3 = ttk.Button(root, text="Start", command=self.on_start_button_click)
        self.button3.pack(side=tk.LEFT, padx=10, pady=10)

        self.button4 = ttk.Button(root, text="Xóa", command=self.on_xoa_button_click)
        self.button4.pack(side=tk.LEFT, padx=10, pady=10)

        self.treeview = ttk.Treeview(root, columns=("Name Application", "ID Application", "Count Thread"))
        self.treeview.heading("Name Application", text="Name Application")
        self.treeview.heading("ID Application", text="ID Application")
        self.treeview.heading("Count Thread", text="Count Thread")
        self.treeview.pack(padx=10, pady=10)


    def on_xem_button_click(self):
        # Your logic for Xem button click goes here
        pass

    def on_kill_button_click(self):
        # Your logic for Kill button click goes here
        pass

    def on_start_button_click(self):
        # Your logic for Start button click goes here
        pass

    def on_xoa_button_click(self):
        self.treeview.delete(*self.treeview.get_children())



    def form_closing(self):
        self.send_message("QUIT")
        self.root.destroy()

    def send_message(self, message):
        if self.client:
            self.client.sendall(message.encode())

    def receive_message(self):
        try:
            response = self.client.recv(1024).decode()
            return response
        except:
            return "Error receiving response"

def mainListApp():
    root = tk.Tk()
    app = ListAppForm(root)
    root.mainloop() 

if __name__ == "__main__":
    mainListApp()
