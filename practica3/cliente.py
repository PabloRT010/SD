import requests
import json


# para comprobar que el dni sea valido
def nif(dni):
    dic = {'T': 0, 'R': 1, 'W': 2, 'A': 3, 'G': 4, 'M': 5, 'Y': 6, 'F': 7, 'P': 8, 'D': 9, 'X': 10, 'B': 11, 'N': 12,
           'J': 13, 'Z': 14, 'S': 15, 'Q': 16, 'V': 17, 'H': 18, 'L': 19, 'C': 20, 'K': 21, 'E': 22}
    # diccionario con las letras y sus respectivos restos
    if len(dni) == 9:  # si el dni tiene 9 caracteres
        letra_control = dni[8].upper()  # nos quedamos con la letra
        digitos = int(dni[:8])  # nos quedamos con los digitos
        for letra, digit in dic.items():  # recorremos diccionario 
            if digit == (digitos % 23) and letra == letra_control:
                # si el resto de dividir los digitos del DNI entre 23 coinciden con el digito del diccionario,
                # asi como la letra
                return "DNI valido"
    return "No valido"


while True:
    while True:
        print("\nElige qué opción desea realizar: ")
        eleccion = int(input(
            "\t 1. Dar de alta un nuevo miembro en el directorio.\n\t 2. Modificar los datos de un miembro.\n\t 3. "
            "Consultar la lista de todos los miembros de la Universidad." 
            "\n\t 4. Hacer consulta por DNI.\n\t 5. Consultar miembros según categoría.\n\t 6. Eliminar miembro ya "
            "existente.\n\t 7. Hacer consulta por nombre.\n\t 8. Hacer consulta por asignatura.\n\t 9. Salir.\n"))
        if eleccion < 10 or eleccion > 0:  # si la eleccion se encuentra entre 1 y 6 (opciones validas)
            break
    if eleccion == 1:
        # dar de alta
        print("Dar de alta un nuevo miembro.")
        while True:
            dni = input("    - DNI: ")  # leemos DNI del usuario
            respuesta = nif(dni)
            if respuesta == "DNI valido":
                break
        nombre = input("    - Nombre completo: ")  # Leemos el nombre del usuario
        correo = input("    - Correo electrónico: ")  # Leemos correo
        departamento = input("    - Departamento: ")  # Leemos el departamento
        while True:
            cat = input("    - Categoria (PAS/PDI/becario): ")  # Leemos la categoria del usuario
            if cat == "PAS" or cat == "PDI" or cat == "becario":  # la categoria debe ser una de las 3
                break
        asig = []
        if cat == "PDI":  # si es PDI debe introducir las asignaturas
            while True:
                asignatura = input("Introduce el nombre de la asignatura: (escribe exit para salir) ")
                if asignatura == 'exit':
                    break
                else:
                    asig.append(asignatura)
        if len(asig) == 0:  # si la lista no tiene asignaturas (usuario no PDI), pongo - (vacio)
            asig.append("-")
        respuesta = requests.post('http://localhost:8080/AddMiembro',
                                  json={'dni': dni, 'nombre': nombre, 'correo': correo, 'departamento': departamento,
                                        'cat': cat, 'asig': asig})
        print(respuesta.text)  # Imprimimos 

    if eleccion == 2:
        dni = input("Introduce el DNI del usuario a modificar: ")
        print("Modificar los datos de un miembro.")
        nombre = input("    - Nombre completo: ")  # Leemos el nombre del usuario
        correo = input("    - Correo electrónico: ")  # Leemos correo
        departamento = input("    - Departamento: ")  # Leemos el departamento
        while True:
            cat = input("    - Categoria (PAS/PDI/becario): ")  # Leemos la categoria del usuario
            if cat == "PAS" or cat == "PDI" or cat == "becario":  # la categoria debe ser una de las 3
                break
        asig = []
        if cat == "PDI":  # si es PDI debe introducir las asignaturas
            while True:
                asignatura = input("Introduce el nombre de la asignatura (escribe exit para salir): ")
                if asignatura == 'exit':
                    break
                else:
                    asig.append(asignatura)
        if len(asig) == 0:  # si la lista no tiene asignaturas (usuario no PDI), pongo - (vacio)
            asig.append("-")

        respuesta = requests.put('http://localhost:8080/ModificarMiembro/' + str(dni),
                                 json={'nombre': nombre, 'correo': correo, 'departamento': departamento, 'cat': cat,
                                       'asig': asig})
        print(respuesta.text)  # Imprimimos 

    if eleccion == 3:
        print("Consultar la lista de todos los miembros de la Universidad.")
        respuesta = requests.get('http://localhost:8080/ListarMiembros')
        print(respuesta.text)  # Imprimimos 

    if eleccion == 4:
        print("Hacer consulta por DNI.")
        dni = input("Introduce el DNI del usuario: ")
        respuesta = requests.get('http://localhost:8080/BuscarMiembro/' + str(dni))
        print(respuesta.text)

    if eleccion == 5:
        print("Consultar miembros según categoría.")
        while True:
            cat = input("Introduce la categoría a consultar: ")  # Leemos la categoria del usuario
            if cat == "PAS" or cat == "PDI" or cat == "becario":  # la categoria debe ser una de las 3
                break

        respuesta = requests.get('http://localhost:8080/ConsultaCat/' + str(cat))
        print(respuesta.text)  # Imprimimos

    if eleccion == 6:
        dni = input("Introduce el DNI del usuario: ")
        respuesta = requests.delete('http://localhost:8080/EliminarMiembro/' + str(dni))
        print(respuesta.text)  # Imprimimos

    if eleccion == 7:
        print("Hacer consulta por nombre.")
        nombre = input("Introduce el nombre del usuario: ")
        respuesta = requests.get('http://localhost:8080/BuscarMiembroNombre/' + str(nombre))
        print(respuesta.text)

    if eleccion == 8:
        print("Hacer consulta por asignatura.")
        asig = input("Introduce el nombre de la asignatura: ")
        respuesta = requests.get('http://localhost:8080/ConsultaAsig/' + str(asig))
        print("Los miembros que pertenecen a la asignatura " + asig + " son:\n " + respuesta.text)

    if eleccion == 9:
        break
