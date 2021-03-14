#! /usr/bin/python3.6
import filecmp
import os

fichero = os.path.isfile('interfaces_bck')
copia = os.path.isfile('/etc/network/interfaces')

if fichero and copia:
	resultado = filecmp.cmp('/etc/network/interfaces', 'interfaces_bck')
	print('Los ficheros son iguales' if resultado else 'Los ficheros no son iguales :(')
	
else:
	print('El fichero /etc/network/interfaces no existe' if fichero else 'El fichero interfaces_bck no existe')

