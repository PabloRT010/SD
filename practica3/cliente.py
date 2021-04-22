import requests
import json

while True:
    while True:
        print("Elige qué opción desea realizar: ")
        eleccion = int(input("\t 1. Dar de alta un nuevo miembro en el directorio.\n\t 2. Modificar los datos de un miembro.\n\t 3. Consultar la lista de todos los miembros de la Universidad." + 
        "\n\t 4. Hacer consulta por DNI.\n\t 5. Consultar miembros según categoría.\n\t 6. Salir.\n"))
        if (eleccion < 7 or eleccion > 0):  # si la eleccion se encuentra entre 1 y 6 (opciones validas)
            break
    if(eleccion == 1):
        #dar de alta
        print("Dar de alta un nuevo miembro.")
        dni = input("    - DNI: ")    # leemos DNI del usuario
        nombre = input("    - Nombre completo: ")  # Leemos el nombre del usuario
        correo = input("    - Corrreo electrónico: ")  # Leemos correo
        departamento = input("    - Departamento: ")  # Leemos el departamento
        while True:
            cat = input("    - Categoria (PAS/PDI/becario): ")    # Leemos la categoria del usuario
            if(cat == "PAS" or cat == "PDI" or cat == "becario"):  # la categoria debe ser una de las 3
                break
        asig = []
        if(cat == "PDI"):  # si es PDI debe introducir las asignaturas
            while True:
                asignatura = input("Introduce el nombre de la asignatura: (escribe exit para salir) ")
                if(asignatura == 'exit'):
                    break
                else:
                    asig.append(asignatura)
        if (len(asig) == 0):  # si la lista no tiene asignaturas (usuario no PDI), pongo - (vacio)
            asig.append("-")
        respuesta = requests.post('http://localhost:8080/AddMiembro', json={'dni' : dni, 'nombre' : nombre, 'correo' : correo, 'departamento' : departamento, 'cat' : cat, 'asig' : asig})
        print(respuesta.text)  # Imprimimos 

    if(eleccion == 2):
        print("Modificar los datos de un miembro.")

    if(eleccion == 3):
        print("Consultar la lista de todos los miembros de la Universidad.")
        respuesta = requests.get('http://localhost:8080/ListarMiembros')
        print(respuesta.text)  # Imprimimos 

    if(eleccion == 4):
        print("Hacer consulta por DNI.")

    if(eleccion == 5):
        print("Consultar miembros según categoría.")


    if(eleccion == 6):
        break
