import socket
HOST = 'localhost'
PORT = 1024
cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # crea socket
cliente.connect((HOST, PORT))  # conexión

cliente.send("Hola, soy el cliente".encode("utf-8"))
mensaje = cliente.recv(1024)

print("Recibido: <<"+mensaje.decode("utf-8")+">> del servidor ")
cliente.close() 
