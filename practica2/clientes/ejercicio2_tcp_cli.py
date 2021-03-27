import socket
import os
import json 
HOST = 'localhost'
PORT = 1024
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))

print("*****Hola, CLIENTE*****")
accion = input("Que desea realizar? \n	1. Enviar fichero.\n	2. Descargar fichero del servidor.\n")
s.send(accion.encode("utf-8"))
if accion == '1': # enviar fichero
	listaFicheros = os.listdir('.')
	hayPDF = 0
	for fich in listaFicheros:
		if '.pdf' in fich: # compruebo si hay ficheros con extension .pdf en el directorio del cliente
			hayPDF += 1

	if hayPDF == 0:
		print("No existen ficheros con la extension .pdf para enviar, cerramos conexion.")
		s.send("NO".encode("utf-8"))
		s.close()

	else: # si exiten .pdfs
		s.send("SI".encode("utf-8")) # aviso al servidor de que existen ficheros para mandar
		print("Los ficheros disponibles para enviar son: ")
		for fich in listaFicheros:
			if '.pdf' in fich:
				print("	○ " + fich)

		FILE = input("Introduce el nombre del fichero: ")
		if FILE not in listaFicheros:
			print("Fichero erroneo. Cerramos conexion.")
			s.send("FAIL".encode("utf-8"))
			s.close()
		else:
			s.send(FILE.encode("utf-8"))
			
			confirmacion = s.recv(1024)		# Espera a la confirmación
			print("Recibo el siguiente mensaje del servidor: " + confirmacion.decode("utf-8"))

			f = open(FILE, "rb")
			chunk = f.read(1024)
			while chunk:
				s.send(chunk)
				chunk = f.read(1024)
			f.close()

			recepcion = s.recv(1024)
			print("Recibo el siguiente mensaje del servidor: " + recepcion.decode("utf-8"))

			os.remove(FILE)

			s.close()

if accion == '2':
	ficherosServidor = s.recv(1024)
	ficherosServidor = json.loads(ficherosServidor) # recibimos lista de ficheros del servidor
	print("Los ficheros disponibles para recibir son: ")
	for fich in ficherosServidor:
		if '.pdf' in fich:
			print("	○ " + fich)
	FILE_S = input("Introduce el nombre del fichero: ")
	if FILE_S not in ficherosServidor:
			print("Fichero erroneo. Cerramos conexion.")
			s.close()
	else:
		s.send(FILE_S.encode("utf-8")) 
		f = open(FILE_S, "wb")
		while True:
			chunk = s.recv(1024)
			f.write(chunk)
			if len(chunk) < 1024:
				print("Fichero recibido.")
				break
		f.close()
	print("Cerramos conexion")
	s.close()
