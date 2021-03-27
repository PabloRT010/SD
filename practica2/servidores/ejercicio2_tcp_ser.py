import socket
import os
import json 
HOST = 'localhost'
PORT = 1024
socketServidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socketServidor.bind((HOST, PORT))

socketServidor.listen(1)
print("*****SERVIDOR*****")
print("Nos quedamos a la espera...")
s_cliente, addr = socketServidor.accept()

eleccion = s_cliente.recv(1024)
if eleccion.decode("utf-8") == '1':  # el cliente envia
    print("El cliente ha elegido enviar un fichero...")
    hayFichero = s_cliente.recv(1024)
    if hayFichero.decode("utf-8") == "SI":
        # recibimos mensaje del fichero
        FILE = s_cliente.recv(1024)
        FILE = FILE.decode("utf-8")
        if FILE == "FAIL":
            print("Algo salio mal. Cerramos conexion")
            s_cliente.close()
            os.remove(FILE)
        else:
            print("Recibo:[" + FILE + "] del cliente con la direccion " + str(addr))

            f = open(FILE, "wb")
            s_cliente.send("Preparado para recibir fichero".encode("utf-8"))
            while True:
                chunk = s_cliente.recv(1024)
                f.write(chunk)
                if len(chunk) < 1024:
                    print("Fichero recibido.")
                    break
            f.close()
            s_cliente.send("Fichero recibido".encode("utf-8"))
            s_cliente.close()
    else:
        print("El cliente no tiene nada para enviar :(. Cerramos conexion")
        s_cliente.close()

if eleccion.decode("utf-8") == '2':  # el cliente recibe fichero
    print("El cliente ha elegido recibir un fichero...")
    listaFicheros = os.listdir('.')
    send_txt = json.dumps(listaFicheros)
    s_cliente.send(send_txt.encode("utf-8"))  # enviamos lista de ficheros al cliente

    fichero = s_cliente.recv(1024)  # recibimos el fichero que el cliente quiere
    fichero = fichero.decode("utf-8")

    f = open(fichero, "rb")
    chunk = f.read(1024)
    while chunk:  # mandamos fichero al cliente
        s_cliente.send(chunk)
        chunk = f.read(1024)
    f.close()
    print("Fichero enviado al cliente")

    s_cliente.close()
socketServidor.close()
