import psutil
import struct
import _json
import signal
import subprocess
import errno
import os


SERVER = "127.0.0.1"
PORT = 5000
ADDRESS = (SERVER, PORT)
FORMAT = 'utf-8'


def startProcess(process_name):

    try:
        subprocess.Popen(process_name, shell=True)
        return "Process '{}' started successfully".format(process_name)
        # return "The process with name '{}' does not exists.".format(process_name)

    except (FileNotFoundError, ModuleNotFoundError, OSError, LookupError) as err:
        return "Error occurred: {}".format(str(err))



def killProcess(pid):
    # try:
    #     os.kill(process_id, signal.SIGTERM)
    #     clientsocket.send("Kill succesful".encode(FORMAT))
    # except OSError as err:
    #     clientsocket.send("Error".encode(FORMAT))
    try:
        process_id = int(pid)
        os.kill(process_id, signal.SIGTERM)
        return "Process with ID {} terminated successfully".format(process_id)
    except ValueError:
        return "Invalid input: '{}' is not a valid process ID".format(pid)
    except ProcessLookupError:
        return "The process with ID {} does not exists".format(process_id)
    except OSError as err:
        return "The process with ID {} is not found".format(pid)



def send_string(client_socket, s):
    # Send the length of the string
    client_socket.sendall(struct.pack('!I', len(s)))
    # Send the string itself
    client_socket.sendall(s.encode(FORMAT))

def listProcess(clientsocket):
    all_pids = psutil.pids()
    numberProcess = len(all_pids)

    clientsocket.sendall(struct.pack('!I', numberProcess))

    for proc in psutil.process_iter():
        try:
            # Get process details as a dictionary
            process = proc.as_dict(attrs=['pid', 'name', 'num_threads'])
            processInfo = f'{process["pid"]},{process["name"]},{process["num_threads"]}'
            send_string(clientsocket, processInfo)
            
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass




# if __name__ == '__main__':
#     listProcess(clie)