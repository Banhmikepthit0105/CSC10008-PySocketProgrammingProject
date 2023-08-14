import tkinter as tk
from tkinter import ttk

class ListAppForm:
    def __init__(self, client):
        self.client = client

        self.root = tk.Tk()
        self.root.title("List Applications")

        self.button1 = tk.Button(self.root, text="Xem", command=self.button1_Click)
        self.button1.pack()

        self.button2 = tk.Button(self.root, text="Kill", command=self.button2_Click)
        self.button2.pack()

        self.button3 = tk.Button(self.root, text="Start", command=self.button3_Click)
        self.button3.pack()

        self.button4 = tk.Button(self.root, text="Xóa", command=self.button4_Click)
        self.button4.pack()

        self.tree = ttk.Treeview(self.root, columns=("Name", "ID", "Count"))
        self.tree.heading("#1", text="Name Application")
        self.tree.heading("#2", text="ID Application")
        self.tree.heading("#3", text="Count Thread")
        self.tree.pack()

        self.root.protocol("WM_DELETE_WINDOW", self.form_closing)

    def start(self):
        self.root.mainloop()

    def button1_Click(self):
        self.send_message("XEM")
        soprocess = int(self.receive_message())
        for _ in range(soprocess):
            s1 = self.receive_message()
            if s1 == "ok":
                s1 = self.receive_message()
                s2 = self.receive_message()
                s3 = self.receive_message()
                self.tree.insert("", "end", values=(s1, s2, s3))

    def button2_Click(self):
        self.send_message("KILL")
        kill_form = KillForm(self.client)
        kill_form.start()

    def button3_Click(self):
        self.send_message("START")
        start_form = StartForm(self.client)
        start_form.start()

    def button4_Click(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

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

class KillForm:
    def __init__(self, client):
        self.client = client
        # Initialize the KillForm GUI components here

    # Implement the rest of the KillForm methods here

class StartForm:
    def __init__(self, client):
        self.client = client
        # Initialize the StartForm GUI components here

    # Implement the rest of the StartForm methods here

if __name__ == "__main__":
    client = None  # Replace this with your actual client socket object
    list_app_form = ListAppForm(client)
    list_app_form.start()
