#! /usr/bin/python3.6

with open('/etc/passwd', 'r') as fichero: #abrimos el fichero /etc/passwd en modo lectura
    for linea in fichero: #por cada linea que tenga el fichero
        valor = linea.split(':') #separo por : ya que el fichero tiene forma xxx:yy:...
        
        if '/home/' in valor[5]: #si existe la cadena /home/ en valor[5], que es donde se encuentra el directorio de inicio de cada usuario
        	print(valor[0] + ' tiene como directorio de inicio:' + valor[5]) 
fichero.close() #cierro fichero
