import socket
HOST = 'localhost'
PORT = 1024
servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  #crea socket
servidor.bind((HOST, PORT))  #enlaza puertos
servidor.listen(1)  #escuchar

print("Servidor a la espera...")
s_cliente, addr = servidor.accept()  #acepta conexion
mensaje = s_cliente.recv(1024)

print("Recibo: <<"+mensaje.decode("utf-8")+">> del cliente con la direccion " + str(addr))
s_cliente.send("Hola, cliente, soy el servidor".encode("utf-8"))
s_cliente.close()
servidor.close() 
