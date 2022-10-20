
# Clase para conectarnos a MongoDB

from urllib import response
import pymongo
from configuracion import variablesMongo


class PyMongo():
    def __init__(self,variables): #host='localhost', db='opensource', port=27017, timeout=1000, user='', password=''
        self.MONGO_DATABASE = variables["bd"]
        self.MONGO_URI = 'mongodb://' + variables["host"] + ':' + str(variables["port"])
        self.MONGO_CLIENT =None
        self.MONGO_RESPUESTA = None
        self.MONGO_TIMEOUT = variables["timeout"]

    def conectar_mongodb(self):
        try:
            self.MONGO_CLIENT = pymongo.MongoClient(self.MONGO_URI, serverSelectionTimeoutMS=self.MONGO_TIMEOUT)
        except Exception as error:
            print("ERROR", error)
        else:
            pass
            # print("Conexión al servidor de MongoDB realizada: ", )
        # finally:


    def desconectar_mongodb(self):
        if self.MONGO_CLIENT:
            self.MONGO_CLIENT.close()

    def consulta_mongodb(self, collection, filtro, atributos={"_id":0}):
        response = {"status": False, "resultado": []}
        self.MONGO_RESPUESTA = self.MONGO_CLIENT[self.MONGO_DATABASE][collection].find(filtro, atributos)
        if self.MONGO_RESPUESTA:
            response["status"] = True
            for reg in self.MONGO_RESPUESTA:
                response["resultado"].append(reg)
        return response
    
    def consulta_general(self, collection, atributos={"_id":0}):
        response = {"status": False, "resultado": []}
        self.MONGO_RESPUESTA = self.MONGO_CLIENT[self.MONGO_DATABASE][collection].find("",atributos)
        if self.MONGO_RESPUESTA:
            response["status"] = True
            for reg in self.MONGO_RESPUESTA:
                response["resultado"].append(reg)
        return response

    # Insertar datos en la coleccion de estudiantes
    def insertar(self, tabla, documento):
        self.MONGO_RESPUESTA = self.MONGO_CLIENT[self.MONGO_DATABASE][tabla].insert_one(documento)
        if self.MONGO_RESPUESTA:
            return {response: True}
        else:
            return  {response: False}
    
    def eliminar(self, tabla, filtro):
        self.MONGO_RESPUESTA = self.MONGO_CLIENT[self.MONGO_DATABASE][tabla].delete_one(filter=filtro)
        if self.MONGO_RESPUESTA:
            return {response: True}
        else:
            return  {response: False}
        
    def eliminar_varios(self, tabla, filtro):
        self.MONGO_RESPUESTA = self.MONGO_CLIENT[self.MONGO_DATABASE][tabla].delete_many(filter=filtro)
        if self.MONGO_RESPUESTA:
            return {response: True}
        else:
            return  {response: False}
    
    

    def actualizar(self, tabla, filtro, documento):
        self.MONGO_RESPUESTA = self.MONGO_CLIENT[self.MONGO_DATABASE][tabla].update_many(filtro, documento)
        if self.MONGO_RESPUESTA:
            return {response: True}
        else:
            return  {response: False}



# obj_MongoDB = PyMongo(variablesMongo)
# obj_MongoDB.conectar_mongodb()
# obj_MongoDB.consulta_mongodb("estudiantes","")
# obj_MongoDB.actualizar("estudiantes", {"control":"18420473"}, {"$set": {"name":"Ochoa Canela Joaquin Jairo"}})