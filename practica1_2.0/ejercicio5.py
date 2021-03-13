#! /usr/bin/python
import os

directorio = os. getcwd()
print('El directorio actual de trabajo es: ' + directorio)


print('Los ficheros que hay en ' + directorio + ' son:')
ficheros = os.listdir('.')
for x in ficheros:
	print(x)
