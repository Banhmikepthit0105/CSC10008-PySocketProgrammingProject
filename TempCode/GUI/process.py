import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import threading

class ProcessApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Process App")

        self.button1 = tk.Button(root, text="Kill Process", command=self.kill_process)
        self.button1.pack()

        self.button2 = tk.Button(root, text="View Processes", command=self.view_processes)
        self.button2.pack()

        self.listbox = tk.Listbox(root)
        self.listbox.pack()

        self.button3 = tk.Button(root, text="Start Process", command=self.start_process)
        self.button3.pack()

        self.button4 = tk.Button(root, text="Clear List", command=self.clear_list)
        self.button4.pack()

        # self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

    def kill_process(self):
        temp = "KILL"
        # Send 'temp' over network (you need to implement the networking part)
        messagebox.showinfo("Kill Process", "Process killed successfully!")

    def view_processes(self):
        temp = "XEM"
        # Send 'temp' over network (you need to implement the networking part)
        processes_data = [("Process 1", "ID1", "Count1"), ("Process 2", "ID2", "Count2"), ("Process 3", "ID3", "Count3")]
        self.listbox.delete(0, tk.END)
        for process in processes_data:
            self.listbox.insert(tk.END, f"Name: {process[0]}, ID: {process[1]}, Count: {process[2]}")

    def start_process(self):
        temp = "START"
        # Send 'temp' over network (you need to implement the networking part)
        messagebox.showinfo("Start Process", "Process started successfully!")

    def clear_list(self):
        self.listbox.delete(0, tk.END)

    def on_closing(self):
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            s = "QUIT"
            # Send 's' over network (you need to implement the networking part)
            self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = ProcessApp(root)
    root.mainloop()
