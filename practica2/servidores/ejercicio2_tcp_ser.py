import socket
HOST = 'localhost'
PORT = 1024
socketServidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socketServidor.bind((HOST, PORT))

socketServidor.listen(1)
print("*****SERVIDOR*****")
print("Nos quedamos a la espera...")
s_cliente, addr = socketServidor.accept()

hayFichero = s_cliente.recv(1024)
if hayFichero.decode("utf-8") == "SI":
    # recibimos mensaje del fichero
    FILE = s_cliente.recv(1024)
    FILE = FILE.decode("utf-8")
    print("Recibo:[" + FILE + "] del cliente con la direccion " + str(addr))

    f = open(FILE, "wb")
    s_cliente.send("Estoy listo".encode("utf-8"))
    while True:
        chunk = s_cliente.recv(1024)
        f.write(chunk)
        if len(chunk) < 1024:
            print("Done Receiving.")
            break
    f.close()
    s_cliente.send("Yata".encode("utf-8"))
    mensaje = s_cliente.recv(1024)
    print("Recibo:["+mensaje.decode("utf-8")+"] del cliente")
    s_cliente.close()
else:
    print("El cliente no tiene nada para enviar :(. Cerramos conexion")
    s_cliente.close()
socketServidor.close()