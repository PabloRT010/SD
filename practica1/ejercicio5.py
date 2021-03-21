#! /usr/bin/python3.6
import os

directorio = os.getcwd()
print('El directorio actual de trabajo es: ' + directorio) #imprimo el directorio de trabajo

print('Los ficheros que hay en ' + directorio + ' son:')
ficheros = os.listdir('.') #obtengo lista de los ficheros existentes en el directorio actual (.)
for x in ficheros: 
	if(os.path.isfile(x)): #si hay carpertas no se van a mostrar
		print(x)

fichero = input('Escriba el nombre del fichero que desea renombrar: ') 

if os.path.isfile(fichero): #si el fichero a renombrar existe, sigue el programa
	renombre = input('Escriba el nuevo nombre del fichero: ')
	if os.path.isfile(renombre): #si el nuevo nombre ya esta siendo utilizado
		print('Imposible renombrar. Conflicto con un fichero que ya existe.')
	else:
		os.rename(fichero, renombre) # en caso contrario se renombra
		print('El fichero ha sido renombrado correctamente.')
		
else: #si el fichero no existiese
	print('El fichero que desea renombrar no existe o es un directorio.')
