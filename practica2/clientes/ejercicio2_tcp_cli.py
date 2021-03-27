import socket
import os
HOST = 'localhost'
PORT = 1024
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))

print("*****Hola, CLIENTE*****")

listaFicheros = os.listdir('.')
hayPDF = 0
for fich in listaFicheros:
	if '.pdf' in fich:
		hayPDF += 1
if hayPDF == 0:
	print("No existen ficheros con la extension .pdf para enviar, cerramos conexion.")
	s.send("NO".encode("utf-8"))
	s.close()

else:
	s.send("SI".encode("utf-8"))
	print("Los ficheros disponibles para enviar son: ")
	for fich in listaFicheros:
		if '.pdf' in fich:
			print("	○ " + fich)

	FILE = input("Introduce el nombre del fichero: ")
	s.send(FILE.encode("utf-8"))
	
	confirmacion = s.recv(1024)		# Espera a la confirmación
	print(confirmacion.decode("utf-8"))

	f = open(FILE, "rb")
	chunk = f.read(1024)
	while chunk:
		s.send(chunk)
		chunk = f.read(1024)
	f.close()
	os.remove(FILE)

	msg = s.recv(1024)
	msg = msg.decode("utf-8")
	print(msg)
	s.send("Po yo tambien".encode("utf-8"))

	s.close()
