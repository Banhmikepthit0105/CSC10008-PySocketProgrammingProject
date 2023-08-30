import tkinter as tk
import socket
import os
import threading
import json
import tkinter
import io
import struct
from PIL import Image, ImageTk
from tkinter import ttk
from tkinter import Button, Entry
from functools import partial
from tkinter import messagebox
from tkinter import filedialog
from tkinter import filedialog

SERVER =  "127.0.0.1"
PORT = 5000
ADDRESS = (SERVER, PORT)
HEADER_SIZE = 1024
FORMAT = 'utf-8'

COLOUR_BACKGROUND = "#0B1F3A"


script_dir = os.path.dirname(__file__)
file_pathApp = os.path.join(script_dir, "tempData\\apprunningData.txt") 

file_pathProcess = os.path.join(script_dir,  "tempData\\processrunningData.txt")

file_pathKeyLogger = os.path.join(script_dir, "tempData\\keylogger.txt" )
    
class info():
    def __init__(self, ID, Name, thread):
        self.ID = ID
        self.arrayInfo = []
        self.Name = Name
        self.thread = thread


class ClientApp(tk.Tk):
    thread = None
    def __init__(self):
        super().__init__()

        self.title("Client")
        self.geometry("372x302")
        self.resizable(width=False, height=False)
        self.thread_lock = threading.Lock()

        disconnect_requested = False
        self.app_thread = None
        self['background'] = COLOUR_BACKGROUND
        self.butApp = tk.Button(self, text="App Running",bg="#FFD66D",fg="#0b0e43", command=self.runListApp_threaded)
        self.butApp.place(x=93, y=64, width=145, height=63)

        self.butConnect = tk.Button(self, text="Kết nối",bg="#FFD66D",fg="#0b0e43",command=lambda : self.connect_to_server_threaded(self.txtIP.get()))
        self.butConnect.place(x=244, y=27, width=100, height=23)

        self.txtIP = Entry(self)
        self.txtIP.place(x=12, y=29, width=226, height=20)
        self.txtIP.insert(tk.END, "Nhập IP")

        self.butTat = tk.Button(self, text="Tắt máy",bg="#FFD66D",fg="#0b0e43", command=self.shutdown)
        self.butTat.place(x=93, y=133, width=48, height=57)

        self.butReg = tk.Button(self, text="Sửa registry",bg="#FFD66D",fg="#0b0e43",)
        self.butReg.place(x=93, y=196, width=198, height=65)

        self.butExit = tk.Button(self, text="Thoát",bg="#FFD66D",fg="#0b0e43", command=self.exit_client)
        self.butExit.place(x=297, y=196, width=47, height=65)

        self.butPic = tk.Button(self, text="Chụp màn hình",bg="#FFD66D",fg="#0b0e43", command=self.open_screenshot_threaded)
        self.butPic.place(x=147, y=133, width=91, height=57)

        self.butKeyLock = tk.Button(self, text="Keystroke",bg="#FFD66D",fg="#0b0e43", command= self.open_keylogger_threaded) #command=self.open_keylogger)
        self.butKeyLock.place(x=244, y=64, width=100, height=126)

        self.butProcess = tk.Button(self, text="Process \n Running",bg="#FFD66D",fg="#0b0e43", command= self.open_processes_threaded)#, command=self.open_processes)
        self.butProcess.place(x=12, y=64, width=75, height=197)


        self.client = None
        self.nw = None
        self.nr = None
        self.lock()
        self.protocol("WM_DELETE_WINDOW", self.close_window)


        self.mainloop()


    def run_in_thread(self, target):
        def wrapper():
            with self.thread_lock:
                target()

        ClientApp.thread = threading.Thread(target=wrapper)
        ClientApp.thread.start()

##-------------------------------------------------------------------------
##-------------------------------------------------------------------------
##-------------------------------------------------------------------------
##-------------------------------------------------------------------------
##-------------------------------------------------------------------------


    def connect_to_server_threaded(self, txtIP):
        # self.run_in_thread(lambda: self.connect_to_server(txtIP))
        threading.Thread(target=self.connect_to_server, args=(txtIP,)).start()


    def open_screenshot_threaded(self):
        # self.run_in_thread(self.open_screenshot)

        threading.Thread(target=self.open_screenshot).start()

    def open_keylogger_threaded(self):
        # self.run_in_thread(self.runKeyStroke)

        threading.Thread(target=self.runKeyStroke).start()

    def open_processes_threaded(self):
        # self.run_in_thread(target=self.runListProcess)

        threading.Thread(target=self.runListProcess).start()

    def runListApp_threaded(self):
        # self.run_in_thread(self.runListApp)
        threading.Thread(target=self.runListApp).start()


    def exitClient_threaded(self, disconnect):
        threading.Thread(target=lambda: self.exit_client(disconnect, )).start()





##-------------------------------------------------------------------------
##-------------------------------------------------------------------------
##-------------------------------------------------------------------------
##-------------------------------------------------------------------------
##-------------------------------------------------------------------------
    # def connect(self, txtIP):
    #         self.client_thread = threading.Thread(target=lambda : self.connect_to_server_threaded(txtIP,))
    #         self.client_thread.start()

    def connect_to_server(self, txtIP):
        if self.client:
            messagebox.showinfo("Message", "System has already connected to server")
            return
        try:
            # server_address = (txtIP, 5000)  # Change this to the server's address
            try:
                server_ip = socket.gethostbyname(txtIP)
            except socket.gaierror:
                messagebox.showerror("Message", "Invalid server IP Address")
                return
            try:
                self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                getIP = str(txtIP)
                server_address = (getIP, 5000)
                self.client.connect(server_address)
                self.nw = self.client.makefile(mode="w")
                self.nr = self.client.makefile(mode="r")

            # self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            # self.client.connect(ADDRESS)
                messagebox.showinfo("Message", "Connected to server successfully")
                self.unlock()
            except Exception as err:
                messagebox.showerror("Message", "Failed to connect to server: " + str(err))
                self.client = None

        except:
            messagebox.showerror("Message", "Failed to connect to server") 
            if self.client:
                self.client.close()
            return
        
        # except Exception as e:
        #     # self.client = None
        #     self.client = None
        #     # self.disconnect_requested = True
 


    def exit_client(self):
        self.close_window()



    def close_window(self):
        if self.client:
            msg = "exitclient"
            self.client.send(msg.encode(FORMAT))
        if not getattr(self, "window_closed", False):
            self.destroy()
            if self.app_thread:
                self.app_thread.join()
            setattr(self, "window_closed", True)
        self.disconnect_requested = True



    def client_closing(self):
        self.exit_client()



        


##------------------------------------------------------------------------------------------------
##------------------------------------------------------------------------------------------------
##------------------------------------------------------------------------------------------------
##------------------------------------------------------------------------------------------------
##------------------------------------------------------------------------------------------------
##------------------------------------------------------------------------------------------------
##------------------------------------------------------------------------------------------------
##------------------------------------------------------------------------------------------------

    def open_screenshot(self) :
        top = tk.Toplevel()
        top.title("Picture App")
        top.geometry("402x300")
        top['background'] = COLOUR_BACKGROUND

        top.resizable(width= False, height = False)
        self.picture = tk.Label(top)
        self.picture.place(x=12, y=22, width=292, height=266)
        top.grab_set()

        # The button for taking a picture and its action
        top.but_take = tk.Button(top, text="Take Picture",bg="#FFD66D",fg="#0b0e43", command= self.take_picture)
        top.but_take.place(x=310, y=22, width=75, height=171)

        # The button for saving the picture and its action
        top.button_save = tk.Button(top, text="Save Picture", bg="#FFD66D",fg="#0b0e43", command= self.save_picture)
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
        top['background'] = COLOUR_BACKGROUND

        top.resizable(width=False, height=False)
        top.geometry("500x350")
        self.picture = tk.Label(top)
        self.picture.place()
        top.grab_set()

        button_width = 80  # Adjust the width of the buttons
        button_height = 40  # Adjust the height of the buttons


        self.button1 = tk.Button(top, text="Xem", bg="#FFD66D",fg="#0b0e43", command=self.on_xem_button_click)
        self.button1.place(x =20, y = 15, width=button_width, height=button_height)


        
        self.button2 = tk.Button(top, text="Kill",  bg="#FFD66D",fg="#0b0e43", command=self.on_kill_button_click)
        self.button2.place(x =140, y = 15, width=button_width, height=button_height)

        self.button3 = tk.Button(top, text="Start", bg="#FFD66D",fg="#0b0e43", command=self.on_start_button_click)
        self.button3.place(x = 264, y = 15, width=button_width, height=button_height)

        self.button4 = tk.Button(top, text="Xóa", bg="#FFD66D",fg="#0b0e43",command=lambda:self.on_xoa_button_click(self.treeApp))
        self.button4.place(x = 389, y = 15, width=button_width, height=button_height)

        cols = ("ID Application", "Name Application", "Count Thread")
        self.treeApp = ttk.Treeview(top, column = cols, height= 10, selectmode = "browse", show = 'headings')
        self.treeApp.column("#1", anchor= tk.CENTER, stretch= 'no', width= 170)
        self.treeApp.heading("#1", text="ID Application")
        self.treeApp.column("#2", anchor= tk.CENTER, stretch= 'no', width = 140)
        self.treeApp.heading("#2", text="Name Application")
        self.treeApp.column("#3", anchor= tk.CENTER, stretch= 'no', width = 130)
        self.treeApp.heading("#3", text="Count Thread")
        self.treeApp.place(x = 23, y= 85)
        tree_scroll = tk.Scrollbar(top, orient= "vertical")
        tree_scroll.configure(command=self.treeApp.yview)
        self.treeApp.configure(yscrollcommand= tree_scroll.set)
        tree_scroll.place(x = 455, y= 86, height= 224)


        

    def open_file_and_populate_treeview(self, treeApp, filename):
        # Clear existing items in the Treeview
        self.treeApp.delete(*treeApp.get_children())

        # Open the file for reading
        with open(filename, 'r') as file:
            for line in file:
                # Split the line into values
                values = line.rstrip().split(',')

                # Insert the values into the Treeview
                # self.treeview.insert('', 'end', values=values)
                self.treeApp.insert('', 'end', values=values)

    def on_xem_button_click(self):
        msg = "showlistapp"
        self.client.send(msg.encode(FORMAT))


        self.treeApp.delete(*self.treeApp.get_children())
        length = struct.unpack('!I', self.client.recv(4))[0]

        # Receive the string itself
        s = self.client.recv(length).decode()
        # Convert the JSON string back to a list
        string_list = json.loads(s)


        with open(file_pathApp, 'w') as f:
            f.truncate(0)

        with open(file_pathApp, 'w', encoding=FORMAT) as f:
            for string in string_list:
                f.write(string + '\n')
                # print(string, " ")
        # print("DONE")
        self.open_file_and_populate_treeview(self.treeApp, file_pathApp)


    def on_kill_button_click(self):


        top= tk.Toplevel()
        top.geometry("250x70")
        top.title("KILL")
        top['background'] = COLOUR_BACKGROUND
        top.grab_set()


        tk.Label(top, text="ID ",bg="#0b0e43",fg="#FFD66D",font='verdana 10 ').place(x = 27, y = 27)
        self.entry_id = tk.Entry(top,width=20)
        top.button = tk.Button(top,text="Kill", bg="#FFD66D",fg="#0b0e43", width= 6, height=1, command=lambda: self.butNhapKILL_Click(self.entry_id)).place(x= 185, y = 27)
        self.entry_id.place(x = 57, y = 30)

        # top.butNhap.grid(row=0, column=1, padx=13, pady=13)



    def butNhapKILL_Click(self, txtID):
            def close_message_box():
                top_message.destroy()
            process_id = txtID.get()
            if process_id:
                # Give the message to the server
                self.client.send("killapprunning".encode(FORMAT))
                self.client.send(process_id.encode(FORMAT))
                
                # Receive the message from the server
                response = self.client.recv(HEADER_SIZE).decode(FORMAT)
                
                # Create a new top-level window for the message box
                top_message = tk.Toplevel()
                top_message.title("Message")
                top_message.geometry("450x100")
                top_message.resizable(width=False, height=False)
                top_message.grab_set()  # Set the message box as a modal window
              
                frame = tk.Frame(top_message, bg="#0b0e43")
                frame.pack(fill="both", expand=True)
                # Create a label to display the response message
                lbl_response = tk.Label(frame, text=response,bg="#0b0e43",fg="#FFD66D")
                lbl_response.pack(padx=10, pady=10)
                # top_message['background'] = COLOUR_BACKGROUND

                # Create an OK button to close the message box
                btn_ok = tk.Button(frame, text="OK",bg="#FFD66D",fg="#0b0e43", command=top_message.destroy)
                btn_ok.pack(pady=5)

                top_message.after(100000, close_message_box)


    def on_start_button_click(self):
        top= tk.Toplevel()
        top.geometry("250x70")
        top.title("START")
        top['background'] = COLOUR_BACKGROUND
        top.grab_set()



        tk.Label(top, text="Name ",bg="#0b0e43",fg="#FFD66D",font='verdana 10 ').place(x = 10, y = 27)
        self.entry_id = tk.Entry(top,width=20)
        top.button = tk.Button(top,text="Start", bg="#FFD66D",fg="#0b0e43", width= 6, height=1, command=lambda: self.butNhapSTART_Click(self.entry_id)).place(x= 185, y = 27)
        self.entry_id.place(x = 57, y = 30)


    def butNhapSTART_Click(self, txtName):
            def close_message_box():
                top_message.destroy()
            app_name = txtName.get()
            if app_name:
                # Give the message to the server
                self.client.send("startapprunning".encode(FORMAT))
                self.client.send(app_name.encode(FORMAT))
                
                # Receive the message from the server
                response = self.client.recv(HEADER_SIZE).decode(FORMAT)
                
                # Create a new top-level window for the message box
                top_message = tk.Toplevel()
                top_message.title("Message")
                top_message.geometry("450x100")
                top_message.resizable(width=False, height=False)
                top_message.grab_set()  # Set the message box as a modal window

                frame = tk.Frame(top_message, bg="#0b0e43")
                frame.pack(fill="both", expand=True)




                lbl_response = tk.Label(frame, text=response, bg="#0b0e43", fg="#FFD66D")
                lbl_response.pack(padx=10, pady=10)

                # Create an OK button to close the message box
                btn_ok = tk.Button(frame, text="OK", bg="#FFD66D", fg="#0b0e43", command=top_message.destroy)
                btn_ok.pack(pady=5)



                top_message.after(100000, close_message_box)



    def on_xoa_button_click(self, treeApp):
        self.treeApp.delete(*treeApp.get_children())





##------------------------------------------------------------------------------------------------
##------------------------------------------------------------------------------------------------
##------------------------------------------------------------------------------------------------
##------------------------------------------------------------------------------------------------
##------------------------------------------------------------------------------------------------
##------------------------------------------------------------------------------------------------



    def runListProcess(self):
        top = tk.Toplevel();
        top.title("Process Running")
        top.resizable(width=False, height=False)
        top.geometry("500x350")
        top['background'] = COLOUR_BACKGROUND
        self.picture = tk.Label(top)
        self.picture.place()


        top.grab_set()

        button_width = 80  # Adjust the width of the buttons
        button_height = 40  # Adjust the height of the buttons


        self.but1 = tk.Button(top, text="Xem",bg="#FFD66D",fg="#0b0e43",  command=lambda: self.listProcess(self.my_tree))
        self.but1.place(x =20, y = 15, width=button_width, height=button_height)

        
        self.but2 = tk.Button(top, text="Kill",bg="#FFD66D",fg="#0b0e43",  command=self.killProcess)
        self.but2.place(x =140, y = 15, width=button_width, height=button_height)

        self.but3 = tk.Button(top, text="Start",bg="#FFD66D",fg="#0b0e43",  command=lambda: self.startProcess(self.my_tree))
        self.but3.place(x = 264, y = 15, width=button_width, height=button_height)

        self.but4 = tk.Button(top, text="Xóa",bg="#FFD66D",fg="#0b0e43",  command=lambda: self.deletelistProcess(self.my_tree))
        self.but4.place(x = 389, y = 15, width=button_width, height=button_height)

        cols = ("ID Process", "Name Process", "Count Thread")
        self.my_tree = ttk.Treeview(top, column = cols, height= 10, selectmode = "browse", show = 'headings')
        self.my_tree.column("#1", anchor= tk.CENTER, stretch= 'no', width= 170)
        self.my_tree.heading("#1", text="ID Process")
        self.my_tree.column("#2", anchor= tk.CENTER, stretch= 'no', width = 140)
        self.my_tree.heading("#2", text="Name Process")
        self.my_tree.column("#3", anchor= tk.CENTER, stretch= 'no', width = 130)
        self.my_tree.heading("#3", text="Count Thread")
        self.my_tree.place(x = 23, y= 85)
        tree_scroll = tk.Scrollbar(top, orient= "vertical")
        tree_scroll.configure(command= self.my_tree.yview)
        self.my_tree.configure(yscrollcommand= tree_scroll.set)
        tree_scroll.place(x = 455, y= 86, height= 224)

    def open_filelistProcess_and_populate_treeview(self, my_tree, filename):
        # Clear existing items in the Treeview
        my_tree.delete(*my_tree.get_children())

        # Open the file for reading
        with open(filename, 'r') as file:
            for line in file:
                # Split the line into values
                values = line.rstrip().split(',')

                # Insert the values into the Treeview
                # self.treeview.insert('', 'end', values=values)
                self.my_tree.insert('', 'end', values=values)


    def listProcess(self, my_tree):
        msg = "showlistprocess"
        self.client.send(msg.encode(FORMAT))

        self.deletelistProcess(my_tree)

        number_of_processes_bytes = self.client.recv(4)
        number_of_processes = struct.unpack('!I', number_of_processes_bytes)[0]

   
        process_data = []

        # Receive and store the process information
        for _ in range(number_of_processes):
            # Receive the length of the process info string
            process_info_length_bytes = self.client.recv(4)
            process_info_length = struct.unpack('!I', process_info_length_bytes)[0]

            # Receive the process info string
            process_info_bytes = self.client.recv(process_info_length)
            process_info = process_info_bytes.decode(FORMAT)

            # Append the process info to the list
            process_data.append(process_info)

        # Write the process information to a file
        with open(file_pathProcess, 'w') as file:
            for info in process_data:
                file.write(info + '\n')

        # Populate the Treeview from the file
        self.open_filelistProcess_and_populate_treeview(my_tree, file_pathProcess)





    def killProcess(self):
        top= tk.Toplevel()
        top.geometry("250x70")
        top.title("KILL")
        top['background'] = COLOUR_BACKGROUND
        top.grab_set()



        top.resizable(width=False, height=False)
        tk.Label(top, text="ID ",bg="#0b0e43",fg="#FFD66D",font='verdana 10 ').place(x = 27, y = 27)
        self.entry_id = tk.Entry(top,width=20)
        top.button = tk.Button(top,text="Kill", bg="#FFD66D",fg="#0b0e43", width= 6, height=1, command=lambda: self.butNhapKILLProcess_Click(self.entry_id)).place(x= 185, y = 27)
        self.entry_id.place(x = 57, y = 30)

    
    def butNhapKILLProcess_Click(self, txtID):
            def close_message_box():
                top_message.destroy()
            process_id = txtID.get()
            if process_id:
                # Give the message to the server
                self.client.send("killprocessrunning".encode(FORMAT))
                self.client.send(process_id.encode(FORMAT))
                
                # Receive the message from the server
                response = self.client.recv(HEADER_SIZE).decode(FORMAT)
                
                # Create a new top-level window for the message box
                top_message = tk.Toplevel()
                top_message.title("Message")
                top_message.geometry("450x100")
                top_message.resizable(width=False, height=False)
                top_message.grab_set()  # Set the message box as a modal window

                frame = tk.Frame(top_message, bg="#0b0e43")
                frame.pack(fill="both", expand=True)
                # Create a label to display the response message
                lbl_response = tk.Label(frame, text=response,bg="#0b0e43",fg="#FFD66D")
                lbl_response.pack(padx=10, pady=10)

                # Create an OK button to close the message box
                btn_ok = tk.Button(frame, text="OK",bg="#FFD66D",fg="#0b0e43", command=top_message.destroy)
                btn_ok.pack(pady=5)

                top_message.after(100000, close_message_box)

    

    def startProcess(self, my_tree):
        top= tk.Toplevel()
        top.geometry("250x70")
        top.title("START")
        top['background'] = COLOUR_BACKGROUND
    
    
        top.grab_set()

        top.resizable(width=False, height=False)
        tk.Label(top, text="Name ",bg="#0b0e43",fg="#FFD66D",font='verdana 10 ').place(x = 10, y = 27)
        self.entry_id = tk.Entry(top,width=20)
        top.button = tk.Button(top,text="Start", bg="#FFD66D",fg="#0b0e43", width= 6, height=1, command=lambda: self.butNhapSTARTPROCESS_Click(self.entry_id)).place(x= 185, y = 27)
        self.entry_id.place(x = 57, y = 30)

    def butNhapSTARTPROCESS_Click(self, txtName):
            def close_message_box():
                top_message.destroy()
            app_name = txtName.get()
            if app_name:
                # Give the message to the server
                self.client.send("startprocessrunning".encode(FORMAT))
                self.client.send(app_name.encode(FORMAT))


                
                # Receive the message from the server
                response = self.client.recv(HEADER_SIZE).decode(FORMAT)
                
                # Create a new top-level window for the message box
                top_message = tk.Toplevel()
                top_message.title("Message")
                top_message.geometry("450x100")
                top_message.resizable(width=False, height=False)
                top_message.grab_set()  # Set the message box as a modal window


                frame = tk.Frame(top_message, bg="#0b0e43")
                frame.pack(fill="both", expand=True)

                # Create a label to display the response message
                lbl_response = tk.Label(frame, text=response,bg="#0b0e43",fg="#FFD66D")
                lbl_response.pack(padx=10, pady=10)

                # Create an OK button to close the message box
                btn_ok = tk.Button(frame, text="OK",bg="#FFD66D",fg="#0b0e43", command=top_message.destroy)
                btn_ok.pack(pady=5)

                top_message.after(100000, close_message_box)




    def deletelistProcess(self, my_tree):
        self.my_tree.delete(*my_tree.get_children())
        with open(file_pathProcess, 'w') as file:
            file.truncate(0)



##------------------------------------------------------------------------------------------------
##------------------------------------------------------------------------------------------------
##------------------------------------------------------------------------------------------------
##------------------------------------------------------------------------------------------------
##------------------------------------------------------------------------------------------------
##------------------------------------------------------------------------------------------------

    def runKeyStroke(self):
        top = tk.Toplevel();
        top.title("Key Stroke")
        top.resizable(width=False, height=False)
        top.geometry("500x335")
        top['background'] = COLOUR_BACKGROUND
        self.picture = tk.Label(top)
        self.picture.place()


        top.grab_set()

        button_width = 80  # Adjust the width of the buttons
        button_height = 40  # Adjust the height of the buttons

        self.button1 = tk.Button(top, text="Hook",bg="#FFD66D",fg="#0b0e43",  command=self.hookKey)
        self.button1.place(x =25, y = 15, width=button_width, height=button_height)

        
        self.button2 = tk.Button(top, text="Unhook",bg="#FFD66D",fg="#0b0e43",  command=self.unhookKey)
        self.button2.place(x =145, y = 15, width=button_width, height=button_height)

        self.button3 = tk.Button(top, text="Print",bg="#FFD66D",fg="#0b0e43",  command=self.printKey)
        self.button3.place(x = 269, y = 15, width=button_width, height=button_height)

        self.button4 = tk.Button(top, text="Delete",bg="#FFD66D",fg="#0b0e43",  command=self.deletelistHook)
        self.button4.place(x = 394, y = 15, width=button_width, height=button_height)


        self.text=tk.Text(top, font=("Consolas, 12"), width= 60, height= 10)
        self.text.place(x = 25, y = 65, height= 250, width= 440)
        top.protocol("WM_DELETE_WINDOW", lambda: self.close_window_keyStroke(top))
    
    def close_window_keyStroke(self, top):
        self.unhookKey()
        self.deletelistHook()
        top.destroy()




    def hookKey(self):
        msg = "hookkeystroke"
        with open (file_pathKeyLogger, 'w') as file:
            file.truncate(0)
        self.client.send(msg.encode(FORMAT))



    def unhookKey(self):
        msg = "unhookkeystroke"
        self.client.send(msg.encode(FORMAT))
        

    def open_file_and_populate_tkText(self, filenam):  
        with open(filenam, 'r') as fo:
            content = fo.read()
        self.text.delete("1.0", tk.END)
        self.text.insert(tk.END, content)


    def printKey(self):
        msg = "printkeystroke"
        self.client.send(msg.encode(FORMAT))



        data_length = int.from_bytes(self.client.recv(4), 'big')
        chunks = []
        bytes_received = 0

        while bytes_received < data_length:
            chunk = self.client.recv(min(data_length - bytes_received, 4096))
            if not chunk:
                raise ConnectionError("Connection lost before receiving all data")    
            chunks.append(chunk)
            bytes_received += len(chunk)

        data = b''.join(chunks).decode(FORMAT)
        with open(file_pathKeyLogger, "a") as fi:
            fi.write(data)
        # print(data)
        self.open_file_and_populate_tkText(file_pathKeyLogger)

    def deletelistHook(self):
        with open (file_pathKeyLogger, 'w') as file:
            file.truncate(0)
        self.text.delete("1.0", tk.END)



##------------------------------------------------------------------------------------------------
##------------------------------------------------------------------------------------------------
##------------------------------------------------------------------------------------------------
##------------------------------------------------------------------------------------------------
##------------------------------------------------------------------------------------------------
##------------------------------------------------------------------------------------------------

    def shutdown(self):
        msg = "shutdownwindow"
        self.client.send(msg.encode(FORMAT))

        


##------------------------------------------------------------------------------------------------
##------------------------------------------------------------------------------------------------
##------------------------------------------------------------------------------------------------
##------------------------------------------------------------------------------------------------
##------------------------------------------------------------------------------------------------
##------------------------------------------------------------------------------------------------





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






