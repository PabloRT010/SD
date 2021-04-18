import socket
HOST = 'localhost'
PORT = 1025
cliente = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
cliente.sendto("Soy el cliente".encode("utf-8"),(HOST, PORT))  # send
cliente.close()  # cerramos socket
