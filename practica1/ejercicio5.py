#/usr/bin/ python3
import subprocess

print('Se encuentra en el directorio:')
subprocess.run(["pwd"])
subprocess.run(["ls"])


print('Escriba el nombre del fichero que desea renombrar:')
fichero = input() 
print('Escriba el nuevo nombre:')
nuevoNombre = input()
resultado2 = subprocess.run(["mv", fichero, nuevoNombre]) 
#while (resultado2.returncode != 0): #si el comando anterior se realizo de forma correcta, devolveria 0 y no entraria en el while
 #   print('Escriba el nombre del fichero que desea renombrar:')
  #  fichero = input()
   # print('Escriba el nuevo nombre:')
   # nuevoNombre = input()
   # resultado2 = subprocess.run(["mv", fichero, nuevoNombre])

