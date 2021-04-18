import socket
import os
import json 
HOST = 'localhost'
PORT = 1024
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))

sobreEscribir = 0 # usaremos como centinela para sobreescribir (o no) más adelante

print("*****Hola, CLIENTE*****")
accion = input("¿Qué desea realizar? \n	1. Enviar fichero.\n	2. Descargar fichero del servidor.\n")
s.send(accion.encode("utf-8"))
if accion == '1':  # enviar fichero
	confirmacion = s.recv(1024)
	print("Recibo <<" +confirmacion.decode("utf-8")+ ">> del servidor")
	listaFicheros = os.listdir('.')
	hayPDF = 0
	for fich in listaFicheros:
		if '.pdf' in fich:  # compruebo si hay ficheros con extensión .pdf en el directorio del cliente
			hayPDF += 1

	if hayPDF == 0:  #no existen pdfs
		print("No existen ficheros con la extensión .pdf para enviar, cerramos conexión.")
		s.send("NO".encode("utf-8"))
		s.close()

	else:  # si exiten .pdfs
		s.send("SI".encode("utf-8"))  # aviso al servidor de que existen ficheros para mandar
		print("Los ficheros disponibles para enviar son: ")
		for fich in listaFicheros:
			if '.pdf' in fich:
				print("	○ " + fich)

		FILE = input("Introduce el nombre del fichero: ")
		if FILE not in listaFicheros:
			print("Fichero erróneo. Cerramos conexión.")
			s.send("FAIL".encode("utf-8"))
			s.close()
		else:  #  si existe el fichero
			s.send(FILE.encode("utf-8"))
			existeFichero = s.recv(1024)
			if(existeFichero.decode("utf-8") == "TRUE"):
				respuesta = input("Ya existe un fichero con ese nombre en el servidor, ¿desea sobreescribir? (S/N) ")
				if (respuesta == "N"):
					sobreEscribir = 1
					s.send("N".encode("utf-8"))
					print("Cerramos conexión")
					s.close()
				else:
					s.send("S".encode("utf-8"))

			# si el fichero ya existe y el cliente selecciona sobreescribirlo o el fichero no existe
			if((existeFichero.decode("utf-8") == "TRUE" and sobreEscribir == 0) or existeFichero.decode("utf-8") != "TRUE"):
				confirmacion = s.recv(1024)		# espera a la confirmación
				print("Recibo el siguiente mensaje del servidor: " + confirmacion.decode("utf-8"))

				f = open(FILE, "rb")
				chunk = f.read(1024) 
				while chunk:  #  mandamos fichero
					s.send(chunk)
					chunk = f.read(1024)
				f.close()

				recepcion = s.recv(1024)
				print("Recibo el siguiente mensaje del servidor: " + recepcion.decode("utf-8"))

				os.remove(FILE)  #  eliminamos fichero
				print("Cerramos conexión")
				s.close()

if accion == '2': #  elige descargar fichero 
	ficherosServidor = s.recv(1024)
	ficherosServidor = json.loads(ficherosServidor)  # recibimos lista de ficheros del servidor
	print("Los ficheros disponibles para recibir son: ")
	for fich in ficherosServidor:
		if '.pdf' in fich:
			print("	○ " + fich)
	FILE_S = input("Introduce el nombre del fichero: ")
	if FILE_S not in ficherosServidor:  #  si el fichero elegido no se encuentra en los disponibles del servidor se cierra la conexión
		print("Fichero erróneo. Cerramos conexión.")
		s.close()
	else:
		s.send(FILE_S.encode("utf-8"))  #  si el fichero se encuentra
		f = open(FILE_S, "wb")
		while True:  #  mientras haya datos escribe en el fichero
			chunk = s.recv(1024) 
			f.write(chunk)
			if len(chunk) < 1024:
				print("Fichero recibido.")
				break
		f.close()
	print("Cerramos conexión")
	s.close()
