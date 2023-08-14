import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from PIL import Image, ImageTk
import io



class PicForm:
    def __init__(self, client):
        self.client = client

        self.root = tk.Tk()
        self.root.title("Screenshot")

        self.butTake = tk.Button(self.root, text="Take Screenshot", command=self.butTake_Click)
        self.butTake.pack()

        self.button1 = tk.Button(self.root, text="Save Screenshot", command=self.button1_Click)
        self.button1.pack()

        self.image_label = tk.Label(self.root)
        self.image_label.pack()

        self.root.protocol("WM_DELETE_WINDOW", self.form_closing)

    def start(self):
        self.root.mainloop()

    def butTake_Click(self):
        self.send_message("TAKE")
        image_data = self.receive_image_data()
        if image_data:
            image = Image.open(io.BytesIO(image_data))
            self.update_image_label(image)

    def button1_Click(self):
        if self.image_label.img:
            save_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png")])
            if save_path:
                self.image_label.img.save(save_path, "PNG")

    def form_closing(self):
        self.send_message("QUIT")
        self.root.destroy()

    def send_message(self, message):
        if self.client:
            self.client.sendall(message.encode())

    def receive_image_data(self):
        try:
            size = int(self.receive_message())
            image_data = b""
            while size > 0:
                data = self.client.recv(min(1024, size))
                if not data:
                    break
                image_data += data
                size -= len(data)
            return image_data
        except:
            return None

    def receive_message(self):
        try:
            response = self.client.recv(1024).decode()
            return response
        except:
            return "Error receiving response"

    def update_image_label(self, image):
        self.image_label.img = ImageTk.PhotoImage(image)
        self.image_label.config(image=self.image_label.img)

if __name__ == "__main__":
    client = None  # Replace this with your actual client socket object
    pic_form = PicForm(client)
    pic_form.start()
