import psutil
import struct
import process
from pywinauto import Desktop


SERVER =  "127.0.0.1"
PORT = 5000
ADDRESS = (SERVER, PORT)
HEADER_SIZE = 1024
FORMAT = 'utf-8'



def killRunningApp(clientsocket, pid):
    process.killProcess(clientsocket, pid)

def checkValidApp(w):
    try:
        full_title = w.window_text()
        if full_title == "Taskbar" or full_title == "": return False
        proc_id = w.process_id()
        process = psutil.Process(proc_id)
        thread_count = process.num_threads()
    except psutil.NoSuchProcess:
        return False 
    if ' - ' in full_title:
        app_name = full_title.rsplit(' - ', 1)[1]
    else:
        app_name = full_title
    return f'{proc_id},{app_name},{thread_count}'

def send_string(client_socket, s):
    # Send the length of the string
    client_socket.sendall(struct.pack('!I', len(s)))
    # Send the string itself
    client_socket.sendall(s.encode(FORMAT))

def send_string_list(client_socket, string_list):
    # Send the total number of strings
    client_socket.sendall(struct.pack('!I', len(string_list)))
    # Send each string
    for s in string_list:
        send_string(client_socket, s)

def listRunningApp(clientsocket):
    windows = Desktop(backend="uia").windows()
    runningApp = []
    for w in windows:
        tmp = checkValidApp(w)
        if (tmp == False) : continue 
        runningApp.append(tmp)
    send_string_list(clientsocket, runningApp)
    print("DONE")
