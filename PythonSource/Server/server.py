# ---------TESTING THE COMUNICATION BETWEEN CLIENT AND SERVER--------------------------

# import socket
# import threading
# import config
# import process
# import runningapp
# from shutdownOS import *
# from keylogger import *
# import os
# from pics import *
# import sys
# from tkinter import *
# import tkinter as tk
# from tkinter import Tk, CENTER
# from tkinter import font
# from tkinter import messagebox
# import tkinter



# SERVER =  "127.0.0.1"
# PORT = 5000
# ADDRESS = (SERVER, PORT)
# HEADER_SIZE = 1024
# FORMAT = 'utf-8'



# DISCONNECT_MESSAGE = "!DISCONNECT"
# COLOUR_BACKGROUND = "#0B1F3A"
# COLOUR_BUTTON = "#435B66"
# COLOUR_AFTER = "#435B66"
# COLOUR_FONT = "#DDE6ED"



# script_dir = os.path.dirname(__file__)
# file_path = os.path.join(script_dir, "tempData\\apprunningData.txt") 

# hook_enabled = True  # Initialize the hook status

# server_running = False


# def runClientSocket(connected):
#     global hook_enabled  # Define a global variable to control hook status

#     while True:
#         try:
#             # while True:
#                 if server_running == False: 
#                     connected.close()
#                     return
#                 data = connected.recv(HEADER_SIZE)
#                 if len(data) > 0:
#                     msg = data.decode(FORMAT)
#                     print("Server received: " + msg)
#                     if (msg == "exitclient"):
#                         print("Disconnect client successfully.")
#                         connected.close()
#                         break
#                     elif (msg == "takepicture"):     
#                         sendScreenShot(connected)
#                     elif (msg == "showlistapp"):
#                         runningapp.listRunningApp(connected)
#                     elif (msg == "killapprunning"):
#                         app_id = connected.recv(HEADER_SIZE).decode(FORMAT)
#                         responseApp = runningapp.killRunningApp(app_id)
#                         connected.send(responseApp.encode(FORMAT))
#                     elif (msg == "startapprunning"):
#                         app_name = connected.recv(HEADER_SIZE).decode(FORMAT)
#                         response = runningapp.startRunningApp(app_name)
#                         connected.send(response.encode(FORMAT))
#                     elif (msg == "showlistprocess"):
#                         process.listProcess(connected)
#                     elif (msg == "killprocessrunning"):
#                         proces_id = connected.recv(HEADER_SIZE).decode(FORMAT)
#                         responseProcess = process.killProcess(proces_id)
#                         connected.send(responseProcess.encode(FORMAT))
#                     elif (msg == "startprocessrunning"):
#                         process_name = connected.recv(HEADER_SIZE).decode(FORMAT)
#                         response = process.startProcess(process_name)
#                         connected.send(response.encode(FORMAT))
#                     elif (msg == "hookkeystroke"):
#                         # recorder = KeyboardActivityRecorder(connected)
#                         # recorder_thread = threading.Thread(target=recorder.start_recording)
#                         # recorder_thread.start()
#                         # hook_enabled = True  # Enable hook
#                         startedKeyLogger()
#                     elif (msg == "unhookkeystroke"):
#                         # recorder.stop_recording()
#                         # recorder.replay_keys()
#                         # recorder_thread.join()
#                         config.hook = False
#                     elif (msg == "printkeystroke"):
#                         sendKeyLogger(connected)
#                     elif (msg == "shutdownwindow"):
#                         my_shutdown()
#         except:
#             print("Client disconnected")
#             config.init()
#             connected.close()


# def start_server():

#     try: 
#         global server
#         server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#         server.bind(ADDRESS)
#         server.listen(1)
#         global server_running
#         server_running = True
#         messagebox.showinfo("Error", "Server has started successfully")
#         while True:
#             print("Waiting for client...")
#             global connected
#             connected, address = server.accept()
#             print("Got a connection from %s" % str(address))

#             client_handler = threading.Thread(target=runClientSocket, args=(connected,))
#             client_handler.start()
#     except Exception as err:
#         messagebox.showinfo("Error", "Server has already opened")
#         return

       

# def start_server_thread():
#     server_thread = threading.Thread(target=start_server)
#     server_thread.start()


# def close_window():
#     global server_running 
#     server.close()
#     server_running= False
#     try:
#         server_running = False
#         menuSever.destroy()
#     except tkinter.TclError as er:
#         print(er)


# menuSever = Tk()
# def menuSeverGUI():
#     menuSever.title('Sever')
#     menuSever.geometry("400x150+1100+300")
#     # menuSever.resizable(width= False, height = False)
#     menuSever['background'] = COLOUR_BACKGROUND
#     fontWord = font.Font(family = "Playfair", size = 11)

#     menuSever.buttonOpen = tk.Button(menuSever, text = 'Open Sever', bg="#FFD66D",fg="#0b0e43",font = fontWord ,command= start_server_thread, width = 10, padx = 10, pady = 15)
#     menuSever.buttonOpen.place(relx = 0.5, rely = 0.5, anchor = CENTER) 





# if __name__ == "__main__":

#     # server_thread = threading.Thread(target=menuSeverGUI)
#     # server_thread.start()
    
#     menuSeverGUI()
#     menuSever.mainloop()
#     menuSever.protocol("WM_DELETE_WINDOW",close_window)

import socket
import threading
import config
import process
import runningapp
from shutdownOS import *
from keylogger import *
import os
from pics import *
import sys
from tkinter import *
import tkinter as tk
from tkinter import Tk, CENTER
from tkinter import font
from tkinter import messagebox
import tkinter



SERVER =  "127.0.0.1"
PORT = 5000
ADDRESS = (SERVER, PORT)
HEADER_SIZE = 1024
FORMAT = 'utf-8'



DISCONNECT_MESSAGE = "!DISCONNECT"
COLOUR_BACKGROUND = "#0B1F3A"
COLOUR_BUTTON = "#435B66"
COLOUR_AFTER = "#435B66"
COLOUR_FONT = "#DDE6ED"



script_dir = os.path.dirname(__file__)
file_path = os.path.join(script_dir, "tempData\\apprunningData.txt") 

hook_enabled = True  # Initialize the hook status

server_running = False
server = None

def runClientSocket(connected):
    global hook_enabled  # Define a global variable to control hook status

    while True:
        try:
            while True:
                # if server_running == False: 
                #     connected.close()
                #     break
                data = connected.recv(HEADER_SIZE)
                if len(data) > 0:
                    msg = data.decode(FORMAT)
                    print("Server received: " + msg)
                    if (msg == "exitclient"):
                        messagebox.showinfo("Message", "Client has disconnected")
                        print("Disconnect client successfully.")
                        # connected.close()
                        break
                    elif (msg == "takepicture"):     
                        sendScreenShot(connected)
                    elif (msg == "showlistapp"):
                        runningapp.listRunningApp(connected)
                    elif (msg == "killapprunning"):
                        app_id = connected.recv(HEADER_SIZE).decode(FORMAT)
                        responseApp = runningapp.killRunningApp(app_id)
                        connected.send(responseApp.encode(FORMAT))
                    elif (msg == "startapprunning"):
                        app_name = connected.recv(HEADER_SIZE).decode(FORMAT)
                        response = runningapp.startRunningApp(app_name)
                        connected.send(response.encode(FORMAT))
                    elif (msg == "showlistprocess"):
                        process.listProcess(connected)
                    elif (msg == "killprocessrunning"):
                        proces_id = connected.recv(HEADER_SIZE).decode(FORMAT)
                        responseProcess = process.killProcess(proces_id)
                        connected.send(responseProcess.encode(FORMAT))
                    elif (msg == "startprocessrunning"):
                        process_name = connected.recv(HEADER_SIZE).decode(FORMAT)
                        response = process.startProcess(process_name)
                        connected.send(response.encode(FORMAT))
                    elif (msg == "hookkeystroke"):
                        # recorder = KeyboardActivityRecorder(connected)
                        # recorder_thread = threading.Thread(target=recorder.start_recording)
                        # recorder_thread.start()
                        # hook_enabled = True  # Enable hook
                        startedKeyLogger()
                    elif (msg == "unhookkeystroke"):
                        # recorder.stop_recording()
                        # recorder.replay_keys()
                        # recorder_thread.join()
                        config.hook = False
                    elif (msg == "printkeystroke"):
                        sendKeyLogger(connected)
                    elif (msg == "shutdownwindow"):
                        my_shutdown()
        except:
            print("Client disconnected")
            config.init()
            # connected.close()
            return


def start_server():

    global server
    try: 
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind(ADDRESS)
        server.listen(5)
        messagebox.showinfo("Message", "Server has started successfully")
        if server_running == False:
            return
        while server_running == True:
            print("Waiting for client...")
            global connected
            connected, address = server.accept()
            print("Got a connection from %s" % str(address))

            client_handler = threading.Thread(target=runClientSocket, args=(connected,))
            client_handler.start()
    
    except Exception as err1:
        messagebox.showinfo("Error", "Server has already started")
       

def start_server_thread():
    global server_thread
    global server_running
    server_running = True
    server_thread = threading.Thread(target=start_server)
    server_thread.start()


def close_server():
    global server_running
    server_running = False  # Signal the server thread to stop
    try:
        if server:
            server.close()  # Close the server socket
            print("Server closed.")
    except tkinter.TclError as err:
        print(err)
    except Exception as e:
        print("Error while closing server:", e)
    # finally:
    #     sys.exit(0)  # Terminate the program


menuSever = Tk()
def close_window():
    try:
        # server.close()
        close_server()
        if 'server_threads' in globals():
            server_thread.join()
        menuSever.destroy()
    except tkinter.TclError as err:
        print(err)


def menuSeverGUI():
    global server_thread  # Declare server_thread as a global variable
    server_thread = None  # Initialize server_thread

    menuSever.title('Sever')
    menuSever.geometry("400x150+1100+300")
    # menuSever.resizable(width= False, height = False)
    menuSever['background'] = COLOUR_BACKGROUND
    fontWord = font.Font(family = "Playfair", size = 11)

    menuSever.buttonOpen = tk.Button(menuSever, text = 'Open Sever', bg="#FFD66D",fg="#0b0e43",font = fontWord ,command= start_server_thread, width = 10, padx = 10, pady = 15)
    menuSever.buttonOpen.place(relx = 0.5, rely = 0.5, anchor = CENTER) 
    menuSever.protocol("WM_DELETE_WINDOW",close_window)





if __name__ == "__main__":

    # server_thread = threading.Thread(target=menuSeverGUI)
    # server_thread.start()
    
    menuSeverGUI()
    menuSever.mainloop()