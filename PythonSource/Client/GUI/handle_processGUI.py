import tkinter as tk
from tkinter import ttk

class process(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("process")

        self.button1 = ttk.Button(self, text="Kill", command=self.button1_Click)
        self.button1.grid(row=0, column=0, padx=10, pady=10)

        self.button2 = ttk.Button(self, text="Xem", command=self.button2_Click)
        self.button2.grid(row=0, column=1, padx=10, pady=10)

        self.button3 = ttk.Button(self, text="Start", command=self.button3_Click)
        self.button3.grid(row=0, column=2, padx=10, pady=10)

        self.button4 = ttk.Button(self, text="Xóa", command=self.button4_Click)
        self.button4.grid(row=0, column=3, padx=10, pady=10)

        self.list_view = ttk.Treeview(self, columns=("name", "id", "count"))
        self.list_view.heading("name", text="Name Process")
        self.list_view.heading("id", text="ID Process")
        self.list_view.heading("count", text="Count Thread")
        self.list_view.grid(row=1, column=0, columnspan=4, padx=10, pady=10)

    def button1_Click(self):
        # Code for button1_Click event
        pass

    def button2_Click(self):
        # Code for button2_Click event
        pass

    def button3_Click(self):
        # Code for button3_Click event
        pass

    def button4_Click(self):
        # Code for button4_Click event
        pass

    def process_closing(self):
        # Code for process_closing event
        pass

# Create an instance of the process class
app = process()

# Run the application
app.mainloop()
