import json
from bottle import run, request, response, get, post, put
# Simulamos base de datos en memoria
miembros = dict() #key: dni, value: miembro
# Creamos una clase Miembro con un constructor que tiene: dni, nombre, correo, departamento, categoria y lista de asignaturas que inicializamos
class Miembro:
    def __init__(self, dni, nombre, correo, departamento, cat, asig):
        self.dni = dni
        self.nombre = nombre
        self.correo = correo
        self.departamento = departamento
        self.cat = cat
        self.asig = asig

@post('/AddMiembro')
def add_miembro():
    data = request.json
    # Datos del JSON
    dni = data.get("dni")
    nombre = data.get("nombre")
    correo = data.get("correo")
    departamento = data.get("departamento")
    cat = data.get("cat")
    asig = data.get("asig")
    miembro = Miembro(dni, nombre, correo, departamento, cat, asig)
    # persistencia (tendríamos que implementar los métodos de conexión con la base de datos etc.)
    # save_data(course)
    # Añadimos instancia a nuestra base de datos
    miembros[dni] = miembro
    # Una vez almacenada la instancia, es conveniente devolver una respuesta al usuario
    # Construimos la cabecera: 'application/json' indicamos que vamos a devolver un JSON
    response.headers['Content-Type'] = 'application/json'
    # Devolvemos el JSON
    return json.dumps({'dni' : dni, 'nombre' : nombre, 'correo' : correo, 'departamento' : departamento, 'cat' : cat, 'asig' : asig})

@put('/ModificarMiembro/<dni_usuario>')
def modificarMiembro(dni_usuario):
    datos = request.json


@get('/ListarMiembros')
def listarmiembros():
    listamiembros = []    #listado de miembros que devolveremos

    for dni_usuario, miembro in miembros.items(): #Recorremos el diccionario por objeto (clave y valor)
        listamiembros.append({'dni' : dni_usuario, 'nombre' : miembro.nombre, 'correo' : miembro.correo, 'departamento' : miembro.departamento, 'cat' : miembro.cat, 'asig' : miembro.asig}) 

    return json.dumps(listamiembros)  #Devolvemos la lista


if __name__ == '__main__':
    run(host='localhost', port=8080, debug=True)
