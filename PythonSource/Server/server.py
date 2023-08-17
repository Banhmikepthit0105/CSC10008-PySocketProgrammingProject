# ---------TESTING THE COMUNICATION BETWEEN CLIENT AND SERVER--------------------------

import socket
import threading
import process
import runningapp
from pics import *

SERVER =  "127.0.0.1"
PORT = 5000
ADDRESS = (SERVER, PORT)
HEADER_SIZE = 1024
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"

def runClientSocket(connected):
    while True:
        try:
            while True:
                data = connected.recv(HEADER_SIZE)
                if len(data) > 0:
                    msg = data.decode(FORMAT)
                    print("Server received: " + msg)
                    if (msg == "takepicture"):     
                        sendScreenShot(connected)
                    if (msg == "showlistapp"):
                        runningapp.listRunningApp(connected)
                    if (msg == "killprocess"):
                        process.killProcess(connected)

        except KeyboardInterrupt:
            connected.close()
        finally:
            connected.close()


def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(ADDRESS)
    server.listen(1)
    while True:
        print("Waiting for client...")
        connected, address = server.accept()
        print("Got a connection from %s" % str(address))
        client_handler = threading.Thread(target=runClientSocket, args=(connected,))
        client_handler.start()

if __name__ == "__main__":
    start_server()
