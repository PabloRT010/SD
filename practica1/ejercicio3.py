#! /usr/bin/python3.6
import filecmp
import os


fichero = os.path.isfile('/etc/network/interfaces')

#copia realizada en el ejercicio 2
copia = os.path.isfile('interfaces_bck') 

#comprueba que ambos ficheros existen
if fichero and copia:
	resultado = filecmp.cmp('/etc/network/interfaces', 'interfaces_bck') #compueba si son iguales 
	print('Los ficheros son iguales' if resultado else 'Los ficheros no son iguales :(')
	
else: #si alguno de los ficheros no existe
	print('El fichero /etc/network/interfaces no existe' if fichero else 'El fichero interfaces_bck no existe')

