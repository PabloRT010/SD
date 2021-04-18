import socket
import os
import pickle
import shutil
HOST = 'localhost'
PORT = 1025
s_udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s_udp.bind((HOST, PORT))
print("Me quedo a la espera")
mensaje, addrCliente = s_udp.recvfrom(1024)
print("Recibido el siguiente mensaje: " + str(mensaje.decode("utf-8")))
print("IP cliente: " + str(addrCliente[0]))
print("Puerto cliente: " + str(addrCliente[1]))

mensaje, addrCliente = s_udp.recvfrom(1024)
print("Recibido el siguiente mensaje: " + str(mensaje.decode("utf-8")))
s_udp.sendto("Listo para recibir".encode("utf-8"), addrCliente)
FILE, addr = s_udp.recvfrom(1024)
FILE = FILE.decode("utf-8")

if FILE == "FAIL":  # si el fichero no existe o no hay pdfs para recibir 
    print("Algo salio mal. Cerramos conexion")
    s_udp.close()
    
else:
    print("Recibo:[" + FILE + "] del cliente")

    f = open(FILE, "wb")
    s_udp.sendto("Preparado para recibir fichero".encode("utf-8"), addrCliente)
    while True:
        data, addr = s_udp.recvfrom(1024)
        f.write(data)
        if len(data) < 1024:
            print("Fichero recibido.")
            break
    f.close()
    s_udp.sendto("Fichero recibido".encode("utf-8"), addrCliente)
    s_udp.close()

    