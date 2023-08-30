import psutil
import struct
import shutil
import os
import threading
import queue
import subprocess
import json
from pywinauto import Desktop


SERVER =  "127.0.0.1"
PORT = 5000
ADDRESS = (SERVER, PORT)
HEADER_SIZE = 1024
FORMAT = 'utf-8'

script_dir = os.path.dirname(__file__)
file_path = os.path.join(script_dir, "tempData\\apprunningData.txt") 


def killRunningApp(appID):
    try:
        app_id = int(appID)
        process = psutil.Process(app_id)
        process.terminate()
        return "Application with ID {} terminated successfully".format(app_id)
    except psutil.NoSuchProcess:
        return "Application with ID {} not found.".format(app_id)
    except Exception as e:
        return "Error occurred: {}".format(str(e))
    
def startRunningApp(appName):
    app_name = str(appName)
    if (shutil.which(app_name)) is None:
        return "Application with name \" {} \" not found ".format(app_name)

    try:
        # Khởi chạy ứng dụng trên máy chủ
        process = subprocess.Popen(app_name, shell=True)
        # Gửi phản hồi cho máy khách
        response = "Application with name {} run successfully".format(app_name)
        return response
    
    except Exception as e:
        return "Error occured: {}".format(str(e))


def checkValidApp(w, q):
    try:
        full_title = w.window_text()
        if full_title == "Taskbar" or full_title == "": 
            q.put(None)
            return
        proc_id = w.process_id()
        process = psutil.Process(proc_id)
        thread_count = process.num_threads()
    except psutil.NoSuchProcess:
        q.put(None)
        return 
    if ' - ' in full_title:
        app_name = full_title.rsplit(' - ', 1)[1]
    else:
        app_name = full_title
    q.put(f'{proc_id},{app_name},{thread_count}')

def send_string(client_socket, s):
    client_socket.sendall(struct.pack('!I', len(s)))
    client_socket.sendall(s.encode('utf-8'))

def send_string_list(client_socket, string_list):
    string_list_json = json.dumps(string_list)
    send_string(client_socket, string_list_json)

def listRunningApp(clientsocket):
    windows = Desktop(backend="uia").windows()
    runningApp = []
    threads = []
    results_queue = queue.Queue()

    for w in windows:
        t = threading.Thread(target=checkValidApp, args=(w,results_queue))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    while not results_queue.empty():
        result = results_queue.get()
        if result is not None:
            runningApp.append(result)

    send_string_list(clientsocket, runningApp)
    print("DONE")