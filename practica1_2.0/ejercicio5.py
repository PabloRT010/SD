#! /usr/bin/python
import os

directorio = os.getcwd()
print('El directorio actual de trabajo es: ' + directorio)


print('Los ficheros que hay en ' + directorio + ' son:')
ficheros = os.listdir('.')
for x in ficheros:
	print(x)

print('Escriba el nombre del fichero que desea renombrar:')
fichero = input()

if os.path.isfile(fichero):
	print('Escriba el nuevo nombre del fichero:')
	renombre = input()
	os.rename(fichero, renombre)
	print('El fichero ha sido renombrado correctamente')
else:
	print('El fichero que desea renombrar no existe')
