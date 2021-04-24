import json
from bottle import run, request, response, get, post, put, delete
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
    try:
        miembros[dni_usuario].nombre = datos.get("nombre")
        miembros[dni_usuario].correo = datos.get("correo")
        miembros[dni_usuario].departamento = datos.get("departamento")
        miembros[dni_usuario].cat = datos.get("cat")
        miembros[dni_usuario].asig = datos.get("asig")
        response.headers['Content-Type'] = 'application/json'
        return json.dumps("Miembro modificado exitosamente.")  # Notificamos al cliente de que ha sido modificada la información del miembro
    except:  # si el miembro no existe
        response.headers['Content-Type'] = 'application/json'
        return json.dumps("Miembro no encontrado.")  # Notificamos al cliente de que ha sido modificada la información del miembro



@get('/ListarMiembros')
def listarmiembros():
    listamiembros = []    # listado de miembros que devolveremos

    for dni_usuario, miembro in miembros.items(): # Recorremos el diccionario por objeto (clave y valor)
        listamiembros.append({'dni' : miembro.dni, 'nombre' : miembro.nombre, 'correo' : miembro.correo, 'departamento' : miembro.departamento, 'cat' : miembro.cat, 'asig' : miembro.asig}) 

    return json.dumps(listamiembros)  # Devolvemos la lista


@get('/BuscarMiembro/<dni>')
def buscarmiembro(dni):
    return json.dumps({'dni' : miembros[dni].dni, 'nombre' : miembros[dni].nombre, 'correo' : miembros[dni].correo, 'departamento' : miembros[dni].departamento, 'cat' : miembros[dni].cat, 'asig' : miembros[dni].asig})  # Devolvemos la lista

@get('/ConsultaCat/<cat>')
def consultacat(cat):
    listamiembros = []
    for dni, miembro in miembros.items(): # Recorremos el diccionario 
        if(miembro.cat == cat):
            listamiembros.append({'dni' : miembro.dni, 'nombre' : miembro.nombre, 'correo' : miembro.correo, 'departamento' : miembro.departamento, 'cat' : miembro.cat, 'asig' : miembro.asig}) 
    return json.dumps(listamiembros)  # Devolvemos la lista


@delete('/EliminarMiembro/<dni>')
def eliminarmiembro(dni):
    try:
        del miembros[dni]
        return json.dumps("Miembro borrado correctamente.")
    except:
        return json.dumps("Algo salió mal.")

if __name__ == '__main__':
    run(host='localhost', port=8080, debug=True)
