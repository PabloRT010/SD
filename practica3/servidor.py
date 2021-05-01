import json
from bottle import run, request, response, get, post, put, delete
import pickle
# Simulamos base de datos en memoria
miembros = dict()  # key: dni
# Creamos una clase Miembro con un constructor que tiene: dni, nombre, correo, departamento, categoria y asignaturas


class Miembro:
    def __init__(self, dni, nombre, correo, departamento, cat, asig):  # inicializamos
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
    for id_miembros in miembros.keys():  # comprobamos que no exista ningun miembro ya registrado con el mismo DNI
        if id_miembros == dni:
            response.headers['Content-Type'] = 'application/json'  # Notificamos de que enviamos un archivo tipo JSON
            return json.dumps("No ha sido posible dar de alta. Ya existe un miembro con ese DNI.")  # notificamos
            # que ya existe un usuario con ese DNI al cliente
    nombre = data.get("nombre")
    correo = data.get("correo")
    departamento = data.get("departamento")
    cat = data.get("cat")
    asig = data.get("asig")
    miembro = Miembro(dni, nombre, correo, departamento, cat, asig)  # creamos el nuevo miembro
    # Añadimos instancia a nuestra base de datos
    miembros[dni] = miembro
    # Indicamos que vamos a devolver un JSON
    response.headers['Content-Type'] = 'application/json'
    # Devolvemos el JSON
    return json.dumps({'dni': dni, 'nombre': nombre, 'correo': correo, 'departamento': departamento, 'cat': cat, 'asig': asig}, indent=2)


@put('/ModificarMiembro/<dni_usuario>')
def modificar_miembro(dni_usuario):
    datos = request.json
    try:  # intentamos modificar la info. del miembro con DNI = dni_usuario
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
        listamiembros.append({'dni': miembro.dni, 'nombre': miembro.nombre, 'correo': miembro.correo,
                              'departamento': miembro.departamento, 'cat': miembro.cat, 'asig': miembro.asig})

    return json.dumps(listamiembros, indent=2)  # Devolvemos la lista


@get('/BuscarMiembro/<dni>')
def buscar_miembro(dni):
    try:  # si el miembro existe devolvemos su info.
        return json.dumps({'dni': miembros[dni].dni, 'nombre': miembros[dni].nombre, 'correo': miembros[dni].correo,
                           'departamento': miembros[dni].departamento, 'cat': miembros[dni].cat, 'asig': miembros[dni].asig}, indent=2)
        # Devolvemos la lista
    except:  # miembro no existe
        return json.dumps("Miembro no encontrado")

@get('/BuscarMiembroNombre/<nombre>')
def buscar_miembro_nombre(nombre):
    listamiembros = []    # listado de miembros que devolveremos

    for dni, miembro in miembros.items():  # Recorremos el diccionario por objeto (clave y valor)
        if miembro.nombre == nombre:  # si el nombre del miembro coincide con el nombre a buscar, incluimos en
            # listamiembros la info. del usuario
            listamiembros.append({'dni': miembro.dni, 'nombre': miembro.nombre, 'correo': miembro.correo,
                                  'departamento': miembro.departamento, 'cat': miembro.cat, 'asig': miembro.asig})
    if len(listamiembros) == 0:  # si la lista mide 0 significa que no se han encontrado usuarios con ese nombre
        return json.dumps("El miembro a buscar no existe")
    else:
        return json.dumps(listamiembros, indent=2)  # Devolvemos la lista

@get('/ConsultaCat/<cat>')
def consulta_cat(cat):
    listamiembros = []
    for dni, miembro in miembros.items():  # Recorremos el diccionario
        if miembro.cat == cat:  # si la categoria del miembro es igual a la cat buscada, lo incluimos en la lista
            listamiembros.append({'dni': miembro.dni, 'nombre': miembro.nombre, 'correo': miembro.correo,
                                  'departamento': miembro.departamento, 'cat': miembro.cat, 'asig': miembro.asig})
    return json.dumps(listamiembros, indent=2)  # Devolvemos la lista


@get('/ConsultaAsig/<asig>')
def consulta_asig(asig):
    listamiembros = []
    for dni, miembro in miembros.items():  # recorremos diccionario
        if miembro.cat == 'PDI':  # si la categoria del miembro es PDI (tiene asignaturas)
            for asignatura in miembro.asig:
                if asignatura == asig:
                    listamiembros.append({'dni': miembro.dni, 'nombre': miembro.nombre, 'correo': miembro.correo,
                                          'departamento': miembro.departamento, 'cat': miembro.cat})
    if len(listamiembros) == 0:
        return json.dumps("No existen miembros con esa asignatura")
    return json.dumps(listamiembros, indent=2)  # Devolvemos la lista



@delete('/EliminarMiembro/<dni>')
def eliminar_miembro(dni):
    try:  # intentamos borrar el mimebro cuyo DNI es el pasado a la funcion
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
