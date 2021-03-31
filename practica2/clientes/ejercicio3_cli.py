import socket
import pickle
HOST = 'localhost'
PORT = 1025
cliente = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
cliente.sendto("Soy el cliente".encode("utf-8"),(HOST, PORT))
while True:
    opciones = ["ls", "rm", "write", "cd", "mv", "exit"]
    while True:
        print("\n\nBienvenido, cliente. Sus opciones son: ")
        print(', '.join(opciones))
        eleccion = input()
        if eleccion in opciones:
            break
        else:
            print("El comando introducido no existe")
    cliente.sendto(eleccion.encode("utf-8"),(HOST, PORT))
    if eleccion == 'ls':
        lista, addr = cliente.recvfrom(1024)
        lista = pickle.loads(lista)
        print("Los ficheros y directorios que se encuentran en el directorio actual del servidor son: ")
        if len(lista) == 0:
            print("El directorio de trabajo se encuentra vacio.")
        else:
            for fichero in lista:
                print(fichero)
    
    if eleccion == 'rm':
        borrar = input("Introduce el nombre del fichero que desea borrar: ")
        cliente.sendto(borrar.encode("utf-8"),(HOST, PORT))
        mensaje, addr = cliente.recvfrom(1024)
        mensaje = mensaje.decode("utf-8")
        print("Recibo el siguiente mensaje del servidor: " + mensaje)

    if eleccion == 'write':
        nombre_fichero = input("Introduce el nombre del fichero que desea crear en el directorio del servidor: ")
        mensaje = input("Introduce el texto del fichero: ")
        cliente.sendto(nombre_fichero.encode("utf-8"),(HOST, PORT))
        cliente.sendto(mensaje.encode("utf-8"),(HOST, PORT))
        mensaje, addr = cliente.recvfrom(1024)
        print("Recibo el siguiente mensaje del servidor: " + mensaje.decode("utf-8"))

    if eleccion == 'cd':
        directorio = input("Introduce el nombre del directorio al que desea cambiarse del servidor: ")
        cliente.sendto(directorio.encode("utf-8"),(HOST, PORT))
        mensaje, addr = cliente.recvfrom(1024)
        print("Recibo el siguiente mensaje del servidor: " + mensaje.decode("utf-8"))
    
    if eleccion == 'mv':
        origen = input("Introduce el origen: ")
        destino = input("Introduce el destino: ")
        cliente.sendto(origen.encode("utf-8"),(HOST, PORT))
        cliente.sendto(destino.encode("utf-8"),(HOST, PORT))
        mensaje, addr = cliente.recvfrom(1024)
        print("Recibo el siguiente mensaje del servidor: " + mensaje.decode("utf-8"))

    if eleccion == 'exit':
        cliente.close()
        break

