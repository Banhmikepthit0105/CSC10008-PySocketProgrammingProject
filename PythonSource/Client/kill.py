import tkinter as tk

class KillForm:
    def __init__(self, client):
        self.client = client

        self.root = tk.Tk()
        self.root.title("Kill Process")

        self.label = tk.Label(self.root, text="Enter Process ID:")
        self.label.pack()

        self.txtID = tk.Entry(self.root)
        self.txtID.pack()

        self.butNhap = tk.Button(self.root, text="Kill", command=self.butNhap_Click)
        self.butNhap.pack()

        self.root.protocol("WM_DELETE_WINDOW", self.form_closing)

    def start(self):
        self.root.mainloop()

    def butNhap_Click(self):
        process_id = self.txtID.get()
        if process_id:
            self.send_message("KILLID")
            self.send_message(process_id)
            response = self.receive_message()
            tk.messagebox.showinfo("Kết quả", response)

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
    client = None  
    kill_form = KillForm(client)
    kill_form.start()
