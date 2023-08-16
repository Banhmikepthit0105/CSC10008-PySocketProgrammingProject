from tkinter import Button, filedialog, Label, Tk
# from PIL import ImageGrab, Image

class PicApp(Tk):
    def __init__(self):
        super().__init__()

        self.title("pic")
        self.geometry("402x300")

        self.picture = Label(self)
        self.picture.place(x=12, y=22, width=292, height=266)

        self.butTake = Button(self, text="Chụp", command=self.take_picture)
        self.butTake.place(x=310, y=22, width=75, height=171)

        self.button1 = Button(self, text="Lưu", command=self.save_picture)
        self.button1.place(x=310, y=219, width=75, height=69)

        self.protocol("WM_DELETE_WINDOW", self.pic_closing)

    def take_picture(self):
        screenshot = ImageGrab.grab()
        new_size = (screenshot.width , screenshot.height )  # Increase the size
        screenshot = screenshot.resize(new_size)  # Resize the image
        self.photo = ImageTk.PhotoImage(screenshot)
        self.picture.config(image=self.photo)

    def save_picture(self):
        filename = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png")])
        if filename:
            screenshot = ImageGrab.grab()
            screenshot.save(filename)

    def pic_closing(self):
        self.destroy()

def mainPics():
    app = PicApp()
    app.mainloop()   

if __name__ == "__main__":
    mainPics()