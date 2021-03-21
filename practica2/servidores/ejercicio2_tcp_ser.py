import socket
HOST = 'localhost'
PORT = 1024
socketServidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socketServidor.bind((HOST, PORT))
socketServidor.listen(1)
print("Nos quedamos a la espera...")
s_cliente, addr = socketServidor.accept()
mensaje = s_cliente.recv(1024)
print("Recibo:["+mensaje.decode("utf-8")+"] del cliente con la direccion " + str(addr))
s_cliente.send("Hola, cliente, soy el servidor".encode("utf-8"))

#recibimos mensaje del fichero
fichero = s_cliente.recv(1024)
print("Recibo:["+fichero.decode("utf-8")+"] del cliente con la direccion " + str(addr))

FILE = s_cliente.recv(1024)
f = open(FILE.strip(), "wb")
while True:
    chunk = s_cliente.recv(1024)
    f.write(chunk)
    if len(chunk) < 1024:
        break
f.close()
print('Fichero recibido.')

s_cliente.close()
socketServidor.close() 
