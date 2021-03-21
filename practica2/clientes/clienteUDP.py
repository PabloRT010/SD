import socket
HOST = 'localhost'
PORT = 1025
s_udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s_udp.sendto("Soy el cliente".encode("utf-8"),(HOST, PORT))
s_udp.close()
