import socket
HOST = 'localhost'
PORT = 1025
s_udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s_udp.bind((HOST, PORT))
print("Me quedo a la espera")
mensaje,addr = s_udp.recvfrom(1024)
print("Recibido el mensaje --->" + str(mensaje.decode("utf-8")))
print("IP cliente: " + str(addr[0]))
print("Puerto cliente: " + str(addr[1]))
s_udp.close()
