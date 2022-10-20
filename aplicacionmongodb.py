
from env import variables
from configuracion import variablesMongo
from crudmysql import MySQL
from mongodb import PyMongo
# from password import Password


def cargar_estudiantes():
    obj_MySQL = MySQL(variables)
    obj_PyMongo = PyMongo(variablesMongo)
    # Crear las consultas
    sql_estudiante = "select * from estudiantes;"
    sql_kardex = "SELECT * FROM kardex;"
    sql_usuario = "SELECT * FROM usuarios;"
    obj_MySQL.conectar_mysql()
    lista_estudiantes = obj_MySQL.consulta_sql(sql_estudiante)
    lista_kardex = obj_MySQL.consulta_sql(sql_kardex)
    lista_usuarios = obj_MySQL.consulta_sql(sql_usuario)
    obj_MySQL.desconectar_mysql()
    # Insertar datos en MongoDB
    obj_PyMongo.conectar_mongodb()
    for est in lista_estudiantes:
        e = {
            'control': est[0],
            'nombre': est[1]
        }
        obj_PyMongo.insertar('estudiantes', e)
    for mat in lista_kardex:
        m = {
            'idKardex': mat[0],
            'control': mat[1],
            'materia': mat[2],
            'calificacion': float(mat[3])
        }
        obj_PyMongo.insertar('kardex', m)
    for usr in lista_usuarios:
        u = {
            'idUsuario': usr[0],
            'control': usr[1],
            'clave': usr[2],
            'clave_cifrada': usr[3]
        }
        obj_PyMongo.insertar('usuarios', u)
    obj_PyMongo.desconectar_mongodb()

def insertar_estudiante():
    obj_PyMongo = PyMongo(variablesMongo)
    print(" == INSERTAR ESTUDIANTES ==")
    ctrl = input("Dame el numero de control: ")
    nombre = input("Dame el nombre del estudiante: ")
    clave = input("Dame la clave de acceso: ")
    # obj_usuario = Password(longitud=len(clave), contrasena=clave)
    json_estudiante = {'control': ctrl, 'nombre': nombre} # f"INSERT INTO estudiantes values('{ctrl}','{nombre}');"
    json_usuario = {'idUsuario':100, 'control':ctrl, 'clave': clave, 'clave_cifrada':clave}# f'INSERT INTO usuarios(control,clave,clave_cifrada) values("{ctrl}","{clave}","{obj_usuario.contrasena_cifrada.decode()}");'
    # print(sql_usuario)
    obj_PyMongo.conectar_mongodb()
    obj_PyMongo.insertar('estudiantes',json_estudiante)
    obj_PyMongo.insertar('usuarios', json_usuario)
    obj_PyMongo.desconectar_mongodb()
    print("Datos insertados correctamente")

def eliminar_estudiante():
    obj_PyMongo = PyMongo(variablesMongo)
    print(" == ELIMINAR ESTUDIANTES ==")
    ctrl = input("Dame el numero de control: ")
    json_estudiante = {'control': ctrl} # f"INSERT INTO estudiantes values('{ctrl}','{nombre}');"
    json_usuario = {'control':ctrl}# f'INSERT INTO usuarios(control,clave,clave_cifrada) values("{ctrl}","{clave}","{obj_usuario.contrasena_cifrada.decode()}");'
    # print(sql_usuario)
    obj_PyMongo.conectar_mongodb()
    obj_PyMongo.eliminar('estudiantes',json_estudiante)
    obj_PyMongo.eliminar('usuarios', json_usuario)
    obj_PyMongo.eliminar_varios('kardex', json_usuario)
    obj_PyMongo.desconectar_mongodb()
    print("Datos Eliminados correctamente")

def actualizar_calificacion():
    obj_PyMongo = PyMongo(variablesMongo)
    print(" == ACTUALIZAR PROMEDIO ==")
    ctrl = input("Dame el numero de control: ")
    materia = input("Dame la materia a actualizar: ")
    filtro_buscar_materia = { 'control': ctrl, 'materia': materia} # f"SELECT 1 FROM kardex" \
                         # f" WHERE control='{ctrl}' AND materia='{materia.strip()}';"
    obj_PyMongo.conectar_mongodb()
    respuesta = obj_PyMongo.consulta_mongodb('kardex', filtro_buscar_materia)
    if respuesta:
        promedio = float(input("Dame el nuevo promedio: "))
        print("Encontrado")
    else:
        print("No Encontrado")
    obj_PyMongo.desconectar_mongodb()
    # if respuesta:
    #     promedio = float(input("Dame el nuevo promedio: "))
    #     sql_actualiza_prom = f"UPDATE kardex set calificacion={promedio} " \
    #                          f"WHERE control='{ctrl}' and materia='{materia.strip()}';"
    #     obj_MySQL.conectar_mysql()
    #     obj_MySQL.consulta_sql(sql_actualiza_prom)
    #     obj_MySQL.desconectar_mysql()
    #     print("Promedia ha sido actualizado")
    # else:
    #     print(f"El estudiante con numero de control {ctrl} o la materia: {materia} NO EXISTE")
    
def consultar_materias():
    obj_PyMongo = PyMongo(variablesMongo)

    print("\n\n == CONSULTAR MATERIAS POR ESTUDIANTE ==\n")
    ctrl = input("Dame el número de control: ")

    filtro = {"control": ctrl}
    atributos_est = {"_id": 0, "nombre": 1}
    atributos_mat = {"_id": 0, "materia": 1, "calificacion": 1}

    # sql_buscar_materias = "SELECT E.nombre, K.materia, K.calificacion FROM estudiantes E, kardex K " \
    #                       f"WHERE K.control='{ctrl}' AND E.control='{ctrl}';"
    # resp = obj_MySQL.consulta_sql(sql_buscar_materias)

    obj_PyMongo.conectar_mongodb()
    respuesta1 = obj_PyMongo.consulta_mongodb('estudiantes', filtro, atributos_est)
    respuesta2 = obj_PyMongo.consulta_mongodb('kardex', filtro, atributos_mat)

    obj_PyMongo.desconectar_mongodb()
    print()
    if respuesta1["status"] and respuesta2["status"]:
        print(respuesta1["resultado"][0]["nombre"])
        for mat in respuesta2["resultado"]:
            print("   ", mat["materia"], mat["calificacion"])
    else:
        print("No encontrado")

def consulta_general():
    obj_PyMongo = PyMongo(variablesMongo)

    print("\n\n == CONSULTAR GENERAL ==\n")

    atributos_est = {"_id": 0, "nombre": 1, "control":1}
    atributos_mat = {"_id": 0, "materia": 1, "calificacion": 1,"control":1}

    # sql_buscar_materias = "SELECT E.nombre, K.materia, K.calificacion FROM estudiantes E, kardex K " \
    #                       f"WHERE K.control='{ctrl}' AND E.control='{ctrl}';"
    # resp = obj_MySQL.consulta_sql(sql_buscar_materias)

    obj_PyMongo.conectar_mongodb()
    respuesta1 = obj_PyMongo.consulta_general('estudiantes', atributos_est)
    respuesta2 = obj_PyMongo.consulta_general('kardex', atributos_mat)

    obj_PyMongo.desconectar_mongodb()
    print()
    if respuesta1["status"] and respuesta2["status"]:
        for estudiante in respuesta1["resultado"]:
            print(estudiante["nombre"])
            for mat in respuesta2["resultado"]:
                if estudiante["control"] == mat["control"]:
                    print("   ", mat["materia"], mat["calificacion"])
    else:
        print("No encontrado")



def menu():
    while True:
        print(" ===============  Menú Principal  ===================")
        print("1. Insertar estudiante ")
        print("2. Actualizar calificación ")
        print("3. Consultar materias por estudiante")
        print("4. Consulta general de estudiantes")
        print("5. Eliminar a un estudiante ")
        print("6. Salir ")
        print("Dame la opcion que deseas? ")
        try:
            opcion = int(input(""))
        except Exception as error:
            print("ERROR: ", error)
            break
        else:
            if opcion == 1:
                insertar_estudiante()
            elif opcion == 2:
                actualizar_calificacion()
            elif opcion == 3:
                consultar_materias()
            elif opcion == 4:
                consulta_general()
            elif opcion == 5:
                eliminar_estudiante()
            elif opcion == 6:
                break
            else:
                print("Opcion incorrecta ")

# cargar_estudiantes()
menu()