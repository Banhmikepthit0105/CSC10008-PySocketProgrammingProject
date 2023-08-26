import tkinter as tk
from tkinter import Button, Entry

class StartApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Start")
        self.geometry("284x51")

        self.butStart = Button(self, text="Start", command=self.start_clicked)
        self.butStart.place(x=197, y=10, width=75, height=23)

        self.txtID = Entry(self)
        self.txtID.insert(0, "Nhập tên")
        self.txtID.place(x=25, y=13, width=155)

        self.protocol("WM_DELETE_WINDOW", self.start_closing)

    def start_clicked(self):
        # Add your logic for the start button click here
        pass

    def start_closing(self):
        # Add your logic for handling form closing here
        self.destroy()



def mainStart():
    app = StartApp()
    app.mainloop()


if __name__ == "__main__":
    mainStart()
