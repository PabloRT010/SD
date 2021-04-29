import json
from bottle import run, request, response, get, post, put, delete
import pickle
# Simulamos base de datos en memoria
miembros = dict()  # key: dni, value: miembro
# Creamos una clase Miembro con un constructor que tiene: dni, nombre, correo, departamento, categoria y asignaturas


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
    for id_miembros in miembros.keys():
        if id_miembros == dni:
            response.headers['Content-Type'] = 'application/json'  # Notificamos de que enviamos un archivo tipo JSON
            return json.dumps("No ha sido posible dar de alta. Ya existe un miembro con ese DNI.")
    nombre = data.get("nombre")
    correo = data.get("correo")
    departamento = data.get("departamento")
    cat = data.get("cat")
    asig = data.get("asig")
    miembro = Miembro(dni, nombre, correo, departamento, cat, asig)
    # Añadimos instancia a nuestra base de datos
    miembros[dni] = miembro
    # Indicamos que vamos a devolver un JSON
    response.headers['Content-Type'] = 'application/json'
    # Devolvemos el JSON
    return json.dumps({'dni': dni, 'nombre': nombre, 'correo': correo, 'departamento': departamento, 'cat': cat, 'asig': asig}, indent=2)


@put('/ModificarMiembro/<dni_usuario>')
def modificar_miembro(dni_usuario):
    datos = request.json
    try:
        miembros[dni_usuario].nombre = datos.get("nombre")
        miembros[dni_usuario].correo = datos.get("correo")
        miembros[dni_usuario].departamento = datos.get("departamento")
        miembros[dni_usuario].cat = datos.get("cat")
        miembros[dni_usuario].asig = datos.get("asig")
        response.headers['Content-Type'] = 'application/json'
        return json.dumps("Miembro modificado exitosamente.")  # Notificamos al cliente de que ha sido modificada la
        # información del miembro
    except:  # si el miembro no existe
        response.headers['Content-Type'] = 'application/json'
        return json.dumps("Miembro no encontrado.")  # Notificamos al cliente de que ha sido modificada la
        # información del miembro


@get('/ListarMiembros')
def listar_miembros():
    listamiembros = []    # listado de miembros que devolveremos

    for dni_usuario, miembro in miembros.items():  # Recorremos el diccionario por objeto (clave y valor)
        listamiembros.append({'dni': miembro.dni, 'nombre': miembro.nombre, 'correo': miembro.correo, 'departamento': miembro.departamento, 'cat': miembro.cat, 'asig': miembro.asig})

    return json.dumps(listamiembros, indent=2)  # Devolvemos la lista


@get('/BuscarMiembro/<dni>')
def buscar_miembro(dni):
    return json.dumps({'dni': miembros[dni].dni, 'nombre': miembros[dni].nombre, 'correo': miembros[dni].correo, 'departamento': miembros[dni].departamento, 'cat': miembros[dni].cat, 'asig': miembros[dni].asig}, indent=2)
    # Devolvemos la lista

@get('/BuscarMiembroNombre/<nombre>')
def buscar_miembro_nombre(nombre):
    listamiembros = []    # listado de miembros que devolveremos

    for dni, miembro in miembros.items():  # Recorremos el diccionario por objeto (clave y valor)
        if miembro.nombre == nombre:
            listamiembros.append({'dni': miembro.dni, 'nombre': miembro.nombre, 'correo': miembro.correo, 'departamento': miembro.departamento, 'cat': miembro.cat, 'asig': miembro.asig})
    if len(listamiembros) == 0:
        return json.dumps("El miembro a buscar no existe")
    return json.dumps(listamiembros, indent=2)  # Devolvemos la lista

@get('/ConsultaCat/<cat>')
def consulta_cat(cat):
    listamiembros = []
    for dni, miembro in miembros.items():  # Recorremos el diccionario
        if miembro.cat == cat:
            listamiembros.append({'dni': miembro.dni, 'nombre': miembro.nombre, 'correo': miembro.correo, 'departamento': miembro.departamento, 'cat': miembro.cat, 'asig': miembro.asig})
    return json.dumps(listamiembros, indent=2)  # Devolvemos la lista


@delete('/EliminarMiembro/<dni>')
def eliminar_miembro(dni):
    try:
        del miembros[dni]
        return json.dumps("Miembro borrado correctamente.")
    except:
        return json.dumps("Algo salió mal.")


def guardar_datos(dic):  # usado para guardar los datos en fichero 
    with open("miembros.dat", "wb") as f:
        pickle.dump(dic, f)


def carga_datos():  # usado para cargar los datos ya existentes en el sistema
    try:
        with open("miembros.dat", "rb") as f:
            return pickle.load(f)
    except (OSError, IOError) as e:
        return dict()


if __name__ == '__main__':
    miembros = carga_datos()
    run(host='localhost', port=8080, debug=True)
    guardar_datos(miembros)
