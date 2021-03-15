#! /usr/bin/python3.6
import os

directorio = os.getcwd()
print('El directorio actual de trabajo es: ' + directorio)

print('Los ficheros que hay en ' + directorio + ' son:')
ficheros = os.listdir('.')
for x in ficheros:
	print(x)

fichero = input('Escriba el nombre del fichero que desea renombrar:')
)

if os.path.isfile(fichero): 
	renombre = input('Escriba el nuevo nombre del fichero:')
	if os.path.isfile(renombre):
		print('Imposible renombrar. El nuevo nombre del fichero ya existe.')
	else:
		os.rename(fichero, renombre)
		print('El fichero ha sido renombrado correctamente.')
		
else: 
	print('El fichero que desea renombrar no existe.')
