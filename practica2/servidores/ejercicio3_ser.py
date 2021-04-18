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
print("Recibido el mensaje <<" + str(mensaje.decode("utf-8")) + ">> del cliente con la dirección: (" + str(addrCliente[0]) + ", " + str(addrCliente[1]) + ")")
while True:
    #  listar ficheros
    listaFichero = os.listdir('.')
    opcion, addrCliente = s_udp.recvfrom(1024)  # elección del cliente

    if opcion.decode("utf-8") == 'ls':   # el cliente elige listar el directorio del servidor
        print("El cliente ha selecionado ls")
        lista = pickle.dumps(listaFichero)  
        # envío de la lista de ficheros
        s_udp.sendto(lista, addrCliente)

    if opcion.decode("utf-8") == 'rm':  # el cliente elige borrar un fichero del directorio del servidor
        print("El cliente ha selecionado rm")
        fichero, addrCliente = s_udp.recvfrom(1024)  # recibe el nombre del fichero del cliente
        try:
            os.remove(fichero)  # intentamos borrar fichero
            s_udp.sendto("El fichero ha sido borrado con éxito".encode("utf-8"), addrCliente)  # enviamos mensaje al cliente
        except FileNotFoundError:  # si el fichero no existe
            s_udp.sendto("El fichero que desea borrar no existe.".encode("utf-8"), addrCliente)  # enviamos mensaje al cliente
        except:  # cualquier otro fallo
            s_udp.sendto("Algo salió mal.".encode("utf-8"), addrCliente)  # enviamos mensaje al cliente

    if opcion.decode("utf-8") == 'write':   # el cliente elige crear un fichero 
        print("El cliente ha selecionado write")
        fichero, addrCliente = s_udp.recvfrom(1024)  # recibimos nombre del fichero
        mensaje, addrCliente = s_udp.recvfrom(1024)  # recibimos informacion del fichero
        f = open(fichero.decode("utf-8"), "w+")
        try:
            f.write(mensaje.decode("utf-8"))  # intentamos escribir en el fichero
            s_udp.sendto("El fichero ha sido creado con éxito".encode("utf-8"), addrCliente)  # enviamos mensaje al cliente
        except:
            s_udp.sendto("Algo salió mal".encode("utf-8"), addrCliente)  # enviamos mensaje al cliente
        finally:
            f.close()  # cerramos fichero
    
    if opcion.decode("utf-8") == 'cd':  # el cliente elige cambiar el directorio del servidor
        print("El cliente ha selecionado cd")
        directorio, addrCliente = s_udp.recvfrom(1024)  # recibimos directorio al que cambiar
        try:
            os.chdir(directorio.decode("utf-8"))  # intentamos cambiar de directorio
            s_udp.sendto("El cambio de directorio ha sido realizado con éxito".encode("utf-8"), addrCliente)  # enviamos mensaje al cliente
        except NotADirectoryError:  # si el destino no es un directorio
            s_udp.sendto("El directorio no existe.".encode("utf-8"), addrCliente)  # enviamos mensaje al cliente
        except:
            s_udp.sendto("Algo salió mal".encode("utf-8"), addrCliente)  # enviamos mensaje al cliente

    if opcion.decode("utf-8") == 'mv':  # el cliente elige mover un fichero
        print("El cliente ha selecionado mv")
        origen, addrCliente = s_udp.recvfrom(1024)
        destino, addrCliente = s_udp.recvfrom(1024)
        try:
            shutil.move(origen.decode("utf-8"), destino.decode("utf-8"))  # intentamos mover el fichero al destino
            s_udp.sendto("La operación ha sido realizada con éxito".encode("utf-8"), addrCliente)  # enviamos mensaje al cliente
        except:
            s_udp.sendto("Algo salió mal".encode("utf-8"), addrCliente)  # enviamos mensaje al cliente

    if opcion.decode("utf-8") == 'exit':  # el cliente decide salir
        print("Cerramos conexión")
        s_udp.close()  # cerramos conexión 
        break
