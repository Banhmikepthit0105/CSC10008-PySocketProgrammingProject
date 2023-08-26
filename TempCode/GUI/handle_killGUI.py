import tkinter as tk

class KillForm(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Kill")
        self.geometry("284x45")

        self.txtID = tk.Entry(self)
        self.txtID.insert(0, "NHẬP ID")
        self.txtID.grid(row=0, column=0, padx=13, pady=13)

        self.butNhap = tk.Button(self, text="Kill", command=self.butNhap_Click)
        self.butNhap.grid(row=0, column=1, padx=13, pady=13)

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

def mainKill():
    app = KillForm()
    app.mainloop()

if __name__ == "__main__":
    mainKill()