import socket
import pickle
import os
HOST = 'localhost'
PORT = 1025
cliente = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
cliente.sendto("Soy el cliente".encode("utf-8"),(HOST, PORT))

cliente.sendto("Voy a enviarte un fichero".encode("utf-8"),(HOST, PORT))
confirmacion, addr = cliente.recvfrom(1024)
print(confirmacion.decode("utf-8"))
print("Los ficheros disponibles para enviar son: ")
listaFichero = os.listdir('.')
numFich = 0
for fich in listaFichero:
	if '.pdf' in fich:
		numFich += 1
		print("	○ " + fich)
if(numFich > 0):
	FILE = input("Introduce el nombre del fichero: ")
	if FILE not in listaFichero:
		print("Fichero erroneo. Cerramos conexion.")
		cliente.sendto("FAIL".encode("utf-8"), addr)
		cliente.close()
	else:  #  si existe el fichero
		cliente.sendto(FILE.encode("utf-8"), addr)
				
		confirmacion, addr = cliente.recvfrom(1024)		# espera a la confirmación
		print("Recibo el siguiente mensaje del servidor: " + confirmacion.decode("utf-8"))

		f = open(FILE, "rb")
		
		while True:  #  mandamos fichero
			chunk = f.read(1024) 
			cliente.sendto(chunk, addr)
			if(len(chunk) < 1024):
				break
			
		f.close()

		recepcion, addr = cliente.recvfrom(1024)
		print("Recibo el siguiente mensaje del servidor: " + recepcion.decode("utf-8"))

		os.remove(FILE)  #  eliminamos fichero
		print("Cerramos conexion")
		cliente.close()
else:
	print("No hay .pdfs para enviar. Cerramos conexion")
	cliente.sendto("FAIL".encode("utf-8"), addr)
	cliente.close()