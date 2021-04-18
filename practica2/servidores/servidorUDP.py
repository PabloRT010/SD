import socket
HOST = 'localhost'
PORT = 1025
servidor = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # crear socket
servidor.bind((HOST, PORT))  

print("Servidor a la espera...")
mensaje,addr = servidor.recvfrom(1024)  # receive
print("Recibido el mensaje <<" + str(mensaje.decode("utf-8")) + ">> del cliente con la dirección: (" + str(addr[0]) + ", " + str(addr[1]) + ")")

servidor.close()  # cerramos socket
