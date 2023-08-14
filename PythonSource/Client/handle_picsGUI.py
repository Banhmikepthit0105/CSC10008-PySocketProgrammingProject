import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk

class pic(tk.Toplevel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.title("pic")
        self.protocol("WM_DELETE_WINDOW", self.pic_closing)

        self.picture = tk.Label(self)
        self.picture.place(x=12, y=22)

        self.butTake = tk.Button(self, text="Chụp", command=self.butTake_Click)
        self.butTake.place(x=310, y=22, width=75, height=171)

        self.button1 = tk.Button(self, text="Lưu", command=self.button1_Click)
        self.button1.place(x=310, y=219, width=75, height=69)

        self.saveFileDialog1 = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png"), ("All files", "*.*")])

    def butTake_Click(self):
        # Implement the logic for taking a screenshot here
        pass

    def button1_Click(self):
        # Implement the logic for saving the image here
        pass

    def pic_closing(self):
        self.destroy()

if __name__ == "__main__":
    app = tk.Tk()
    pic_window = pic(app)
    app.mainloop()
