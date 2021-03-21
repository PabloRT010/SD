import socket, os
HOST = 'localhost'
PORT = 1024
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))
s.send("Hola, servidor".encode("utf-8"))
mensaje = s.recv(1024)
print("Recibido:["+mensaje.decode("utf-8")+"] del servidor ")


s.send(("Hola, servidor, quiero enviarte el fichero: ").encode("utf-8"))
FILE = "hola.pdf"
s.send(FILE.encode("utf-8"))

f = open(FILE, "rb")
chunk = f.read(1024)
while chunk:
	s.send(chunk)
	chunk = f.read(1024)
f.close()


s.close() 