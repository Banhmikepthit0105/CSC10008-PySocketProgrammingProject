import tkinter as tk
from tkinter import messagebox
import socket
from tkinter import Button, Entry

from pics import *
from listApp import *

SERVER =  "127.0.0.1"
PORT = 5000
ADDRESS = (SERVER, PORT)
HEADER_SIZE = 1024
FORMAT = 'utf-8'


class ClientApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Client")
        self.geometry("372x302")

        # self.opened_windows = []  # Danh sách các cửa sổ con đã mở


        self.butApp = tk.Button(self, text="App Running", command=self.runListApp)
        self.butApp.place(x=93, y=64, width=145, height=63)

        self.butConnect = tk.Button(self, text="Kết nối",command=self.connect_to_server)
        self.butConnect.place(x=244, y=27, width=100, height=23)

        self.txtIP = Entry(self)
        self.txtIP.place(x=12, y=29, width=226, height=20)
        self.txtIP.insert(tk.END, "Nhập IP")

        self.butTat = tk.Button(self, text="Tắt máy", command=self.shutdown)
        self.butTat.place(x=93, y=133, width=48, height=57)

        self.butReg = tk.Button(self, text="Sửa registry")
        self.butReg.place(x=93, y=196, width=198, height=65)

        self.butExit = tk.Button(self, text="Thoát")# command=self.exit_client)
        self.butExit.place(x=297, y=196, width=47, height=65)

        self.butPic = tk.Button(self, text="Chụp màn hình", command=self.open_screenshot)
        self.butPic.place(x=147, y=133, width=91, height=57)

        self.butKeyLock = tk.Button(self, text="Keystroke") #command=self.open_keylogger)
        self.butKeyLock.place(x=244, y=64, width=100, height=126)

        self.butProcess = tk.Button(self, text="Process Running")#, command=self.open_processes)
        self.butProcess.place(x=12, y=64, width=75, height=197)


        self.client = None
        self.nw = None
        self.nr = None
        self.lock()

        self.protocol("WM_DELETE_WINDOW", self.client_closing)




    def connect_to_server(self):
        if self.client:
            messagebox.showinfo("Info", "Already connected to server.")
            return

        try:
            self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.client.connect(ADDRESS)
            self.nw = self.client.makefile(mode="w")
            self.nr = self.client.makefile(mode="r")
            messagebox.showinfo("Info", "Connected to server successfully.")
            self.unlock()
        except Exception as e:
            messagebox.showerror("Error", "Failed to connect to server: " + str(e))
            self.client = None

    # def open_applications(self):
    #     if not self.client:
    #         messagebox.showinfo("Info", "Not connected to server.")
    #         return
        
    #     runListAppss = runListApp()


    def take_picture(self):
        if not self.client:
            messagebox.showinfo("Info", "Not connected to server.")
            return
        
        # self.nw.write("takepicture\n")
        # self.nw.flush()
        runPicApp = self.open_screenshot()


    def open_keylogger(self):
        if not self.client:
            messagebox.showinfo("Info", "Not connected to server.")
            return

        self.nw.write("KEYLOG\n")
        self.nw.flush()
        viewKeylog = Keylog(self.nw, self.nr)
        viewKeylog.wait_window()

    def open_processes(self):
        if not self.client:
            messagebox.showinfo("Info", "Not connected to server.")
            return

        self.nw.write("PROCESS\n")
        self.nw.flush()
        viewProcess = Process(self.nw, self.nr)
        viewProcess.wait_window()

    

    def exit_client(self):
        if self.client:
            self.nw.write("QUIT\n")
            self.nw.flush()
            self.client.close()

        self.destroy()

    def client_closing(self):
        if self.client:
            self.nw.write("QUIT\n")
            self.nw.flush()
            self.client.close()
        self.destroy()




    def shutdown(self):
        pass


##------------------------------------------------------------------------------------------------
##------------------------------------------------------------------------------------------------
##------------------------------------------------------------------------------------------------
##------------------------------------------------------------------------------------------------
##------------------------------------------------------------------------------------------------
##------------------------------------------------------------------------------------------------
##------------------------------------------------------------------------------------------------
##------------------------------------------------------------------------------------------------

    def open_screenshot(self) :
        top = tk.Toplevel();
        top.title("Picture App")
        top.geometry("402x300")
        top.resizable(width= False, height = False)
        self.picture = tk.Label(top)
        self.picture.place(x=12, y=22, width=292, height=266)
        top.grab_set()

        # The button for taking a picture and its action
        top.but_take = tk.Button(top, text="Take Picture", command= self.take_picture)
        top.but_take.place(x=310, y=22, width=75, height=171)

        # The button for saving the picture and its action
        top.button_save = tk.Button(top, text="Save Picture", command= self.save_picture)
        top.button_save.place(x=310, y=219, width=75, height=69)


    def take_picture(self):
        s = "takepicture"
        self.client.send(s.encode(FORMAT))
        size = struct.unpack('!I', self.client.recv(4))[0]



        received_data = b''
        while len(received_data) < size:
            data = self.client.recv(1024)
            received_data += data

        self.image = Image.open(io.BytesIO(received_data))
        self.photo = ImageTk.PhotoImage(self.image)
        self.picture.config(image=self.photo)
        # self.picture.image = self.photo  # Keep a reference to the image object
    def save_picture(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png"), ("All files", "*.*")])
        if file_path:
            self.image.save(file_path, format="PNG")


##------------------------------------------------------------------------------------------------
##------------------------------------------------------------------------------------------------
##------------------------------------------------------------------------------------------------
##------------------------------------------------------------------------------------------------
##------------------------------------------------------------------------------------------------
##------------------------------------------------------------------------------------------------

    def runListApp(self):
        top = tk.Toplevel();
        top.title("App Running")
        top.resizable(width=False, height=False)
        self.picture = tk.Label(top)
        self.picture.place()


        self.button1 = ttk.Button(top, text="Xem", command=self.on_xem_button_click)
        self.button1.pack(side=tk.LEFT, padx=10, pady=10)

        
        self.button2 = ttk.Button(top, text="Kill", command=self.on_kill_button_click)
        self.button2.pack(side=tk.LEFT, padx=10, pady=10)

        self.button3 = ttk.Button(top, text="Start", command=self.on_start_button_click)
        self.button3.pack(side=tk.LEFT, padx=10, pady=10)

        self.button4 = ttk.Button(top, text="Xóa", command=self.on_xoa_button_click)
        self.button4.pack(side=tk.LEFT, padx=10, pady=10)

        self.treeview = ttk.Treeview(top, columns=("Name Application", "ID Application", "Count Thread"))
        self.treeview.heading("Name Application", text="Name Application")
        self.treeview.heading("ID Application", text="ID Application")
        self.treeview.heading("Count Thread", text="Count Thread")
        self.treeview.pack(padx=10, pady=10)

    
    def on_xem_button_click(self):
        msg = "showlistapp"
        self.client.send(msg.encode(FORMAT))
        # Receive the length of the incoming data
        data_len = struct.unpack('!I', self.client.recv(4))[0]
        
        # Receive the actual data and decode it
        data = self.client.recv(data_len).decode('latin-1')
        
        # Clear existing items in the treeview
        self.treeview.delete(*self.treeview.get_children())
        
        # Process the received data and update the treeview
        lines = data.split('\n')
        for line in lines:
            if line:
                parts = line.split(',')
                if len(parts) == 3:
                    app_name, app_id, thread_count = parts
                    self.treeview.insert('', 'end', values=(app_name, app_id, thread_count))


        # Send 'temp' over network (you need to implement the networking part)
        # processes_data = [("Process 1", "ID1", "Count1"), ("Process 2", "ID2", "Count2"), ("Process 3", "ID3", "Count3")]
        # self.listbox.delete(0, tk.END)
        # for process in processes_data:
        #     self.listbox.insert(tk.END, f"Name: {process[0]}, ID: {process[1]}, Count: {process[2]}")

    def on_kill_button_click(self):
        temp = "KILL"
        # Send 'temp' over network (you need to implement the networking part)
        messagebox.showinfo("Kill Process", "Process killed successfully!")

    def on_start_button_click(self):
        temp = "START"
        # Send 'temp' over network (you need to implement the networking part)
        messagebox.showinfo("Start Process", "Process started successfully!")

    def on_xoa_button_click(self):
        self.listbox.delete(0, tk.END)


##------------------------------------------------------------------------------------------------
##------------------------------------------------------------------------------------------------
##------------------------------------------------------------------------------------------------
##------------------------------------------------------------------------------------------------
##------------------------------------------------------------------------------------------------
##------------------------------------------------------------------------------------------------



    # lock key
    def lock(self):
        self.butPic.config(state= tk.DISABLED)
        self.butTat.config(state= tk.DISABLED)
        self.butReg.config(state= tk.DISABLED)
        self.butExit.config(state= tk.DISABLED)
        self.butKeyLock.config(state= tk.DISABLED)
        self.butProcess.config(state= tk.DISABLED)
        self.butConnect.config(state= tk.NORMAL)
        self.txtIP.config(state= tk.NORMAL)
        self.butApp.config(state= tk.DISABLED)

    def unlock(self):
        self.butPic.config(state= tk.NORMAL)
        self.butTat.config(state= tk.NORMAL)
        self.butReg.config(state= tk.NORMAL)
        self.butExit.config(state= tk.NORMAL)
        self.butKeyLock.config(state= tk.NORMAL)
        self.butProcess.config(state= tk.NORMAL)
        self.butConnect.config(state= tk.DISABLED)
        self.txtIP.config(state= tk.DISABLED)
        self.butApp.config(state= tk.NORMAL)
    



if __name__ == "__main__":
    app = ClientApp()
    app.mainloop()
