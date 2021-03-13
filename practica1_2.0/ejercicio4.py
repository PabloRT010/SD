#! /usr/bin/python

with open('/etc/passwd', 'r') as fichero:
    for linea in fichero:
        valor = linea.split(':')
        print( valor[0] + ' tiene como directorio de inicio:' + valor[5]) 
