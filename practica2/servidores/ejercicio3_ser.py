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
print("Recibido el mensaje <<" + str(mensaje.decode("utf-8")) + ">> del cliente con la direccion: (" + str(addrCliente[0]) + ", " + str(addrCliente[1]) + ")")
while True:
    #  listar ficheros
    listaFichero = os.listdir('.')
    opcion, addrCliente = s_udp.recvfrom(1024)  # eleccion del cliente

    if opcion.decode("utf-8") == 'ls':   # el cliente elige listar el directorio del servidor
        print("El cliente ha selecionado ls")
        lista = pickle.dumps(listaFichero)  # envio de la lista de ficheros
        s_udp.sendto(lista, addrCliente)

    if opcion.decode("utf-8") == 'rm':  # el cliente elige borrar un fichero del directorio del servidor
        print("El cliente ha selecionado rm")
        fichero, addrCliente = s_udp.recvfrom(1024)  # recibe el nombre del fichero del cliente
        try:
            os.remove(fichero)  # intentamos borrar fichero
            s_udp.sendto("El fichero ha sido borrado con exito".encode("utf-8"), addrCliente)
        except FileNotFoundError:  # si el fichero no existe
            s_udp.sendto("El fichero que desea borrar no existe.".encode("utf-8"), addrCliente)
        except:  # cualquier otro fallo
            s_udp.sendto("Algo salio mal.".encode("utf-8"), addrCliente)

    if opcion.decode("utf-8") == 'write':   # el cliente elige crear un fichero 
        print("El cliente ha selecionado write")
        fichero, addrCliente = s_udp.recvfrom(1024)
        mensaje, addrCliente = s_udp.recvfrom(1024)
        f = open(fichero.decode("utf-8"), "w+")
        try:
            f.write(mensaje.decode("utf-8"))  # intentamos escribir en el fichero
            s_udp.sendto("El fichero ha sido creado con exito".encode("utf-8"), addrCliente)
        except:
            s_udp.sendto("Algo salio mal".encode("utf-8"), addrCliente)
        finally:
            f.close()
    
    if opcion.decode("utf-8") == 'cd':  # el cliente elige cambiar el directorio del servidor
        print("El cliente ha selecionado cd")
        directorio, addrCliente = s_udp.recvfrom(1024)
        try:
            os.chdir(directorio.decode("utf-8"))  # intentamos cambiar de directorio
            s_udp.sendto("El cambio de directorio ha sido realizado con exito".encode("utf-8"), addrCliente)
        except NotADirectoryError:  # si el destino no es un directorio
            s_udp.sendto("El directorio no existe.".encode("utf-8"), addrCliente)
        except:
            s_udp.sendto("Algo salio mal".encode("utf-8"), addrCliente)

    if opcion.decode("utf-8") == 'mv':  # el cliente elige mover un fichero
        print("El cliente ha selecionado mv")
        origen, addrCliente = s_udp.recvfrom(1024)
        destino, addrCliente = s_udp.recvfrom(1024)
        try:
            shutil.move(origen.decode("utf-8"), destino.decode("utf-8"))
            s_udp.sendto("La operacion ha sido realizada con exito".encode("utf-8"), addrCliente)
        except:
            s_udp.sendto("Algo salio mal".encode("utf-8"), addrCliente)

    if opcion.decode("utf-8") == 'exit':
        print("Cerramos conexion")
        s_udp.close()
        break
