import tkinter as tk
from tkinter import Button, Entry, messagebox

class KillForm(tk.Tk):
    def __init__(self, nw, nr):
        super().__init__()

        self.nw = nw
        self.nr = nr

        self.title("Kill")
        self.geometry("300x100")

        self.txtID = Entry(self)
        self.txtID.pack()

        self.butNhap = Button(self, text="Nhap", command=self.butNhap_Click)
        self.butNhap.pack()

        # self.protocol("WM_DELETE_WINDOW", self.kill_closing)

    def butNhap_Click(self):
        self.nw.write("KILLID\n")
        self.nw.write(self.txtID.get() + "\n")
        self.nw.flush()

        s = self.nr.readline().strip()
        messagebox.showinfo("Thông báo", s)

    def kill_closing(self):
        self.nw.write("QUIT\n")
        self.nw.flush()
        self.destroy()

if __name__ == "__main__":
    app = KillForm(None, None)  # Replace None with actual nw and nr streams
    app.mainloop()
