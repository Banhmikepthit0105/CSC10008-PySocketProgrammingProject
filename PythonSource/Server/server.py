#---------TESTING THE COMUNICATION BETWEEN CLIENT AND SERVER--------------------------

# import socket
# import threading

# SERVER =  "127.0.0.1"
# PORT = 5000
# ADDRESS = (SERVER, PORT)
# HEADER_SIZE = 1024
# FORMAT = 'utf-8'
# DISCONNECT_MESSAGE = "!DISCONNECT"

# server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# server.bind(ADDRESS)
# server.listen(1)
# print("waiting for client")
# connected, address = server.accept()

# # try:
# #     while True:
# #         data = connected.recv(HEADER_SIZE)  
# #         if len(data) > 0:
# #             print("Server received: " + data.decode("utf-8") )
# # except KeyboardInterrupt:
# #     connected.close()
# #     server.close()
# # finally:
# #     connected.close()
# #     server.close()



# def handle_client(connected, address):
#     print(f"[NEW CONNECTION] {address} connected")

#     while True:
#         message_length = connected.recv(HEADER_SIZE).decode(FORMAT)
#         if (message_length):
#             message_length = int(message_length)
#             message = connected.recv(message_length).decode(FORMAT)
#             if message == DISCONNECT_MESSAGE:
#                 connected.close()
#                 break;
#         print(f"[{address}:] {message}")
#     print(f"[DISCONNECTED] {address} disconnected")


# def start():
#     server.listen(1)
#     while True:
#         connected, address = server.accept()
#         thread = threading.Thread(target = handle_client, args= (connected, address))
#         thread.start()
#         print(f"[ACTIVATE CONNECTION], Server is connected by {threading.active_count() - 1}")

# print("[STARTING] Server is waiting for client")
# start()    