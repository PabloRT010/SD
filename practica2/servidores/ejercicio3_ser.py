import socket
import os
import pickle
import shutil
HOST = 'localhost'
PORT = 1025
s_udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s_udp.bind((HOST, PORT))
print("Me quedo a la espera")
mensaje,addrCliente = s_udp.recvfrom(1024)
print("Recibido el mensaje --->" + str(mensaje.decode("utf-8")))
print("IP cliente: " + str(addrCliente[0]))
print("Puerto cliente: " + str(addrCliente[1]))
while True:
    #  listar ficheros
    listaFichero = os.listdir('.')
    opcion,addrCliente = s_udp.recvfrom(1024) #  eleccion del cliente

    if opcion.decode("utf-8") == 'ls': 
        lista = pickle.dumps(listaFichero)
        s_udp.sendto(lista, addrCliente)

    if opcion.decode("utf-8") == 'rm': 
        fichero,addrCliente = s_udp.recvfrom(1024) #  recibe el nombre del fichero del cliente
        try:
            os.remove(fichero)
            s_udp.sendto("El fichero ha sido borrado con exito".encode("utf-8"), addrCliente)
        except FileNotFoundError:
            s_udp.sendto("El fichero que desea borrar no existe.".encode("utf-8"), addrCliente)
        except:
            s_udp.sendto("Algo salio mal.".encode("utf-8"), addrCliente)

    if opcion.decode("utf-8") == 'write':
        fichero,addrCliente = s_udp.recvfrom(1024) 
        mensaje,addrCliente = s_udp.recvfrom(1024) 
        f = open(fichero.decode("utf-8"), "w+")
        try:
            f.write(mensaje.decode("utf-8"))
            s_udp.sendto("El fichero ha sido creado con exito".encode("utf-8"), addrCliente)
        except:
            s_udp.sendto("Algo salio mal".encode("utf-8"), addrCliente)
        finally:
            f.close()
    
    if opcion.decode("utf-8") == 'cd':
        directorio,addrCliente = s_udp.recvfrom(1024) 
        try:
            os.chdir(directorio.decode("utf-8"))
            s_udp.sendto("El cambio de directorio ha sido realizado con exito".encode("utf-8"), addrCliente)
        except NotADirectoryError:
            s_udp.sendto("El directorio no existe.".encode("utf-8"), addrCliente)
        except:
            s_udp.sendto("Algo salio mal".encode("utf-8"), addrCliente)

    if opcion.decode("utf-8") == 'mv':
        origen, addrCliente = s_udp.recvfrom(1024)
        destino, addrCliente = s_udp.recvfrom(1024)
        try:
            shutil.move(origen.decode("utf-8"), destino.decode("utf-8"))
            s_udp.sendto("La operacion ha sido realizada con exito".encode("utf-8"), addrCliente)
        except:
            s_udp.sendto("Algo salio mal".encode("utf-8"), addrCliente)


    if opcion.decode("utf-8") == 'exit': 
        s_udp.close()
        break