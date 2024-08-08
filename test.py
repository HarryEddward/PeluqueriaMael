from pymongo import MongoClient
from pymongo.errors import ServerSelectionTimeoutError, ConfigurationError

from Backend.microservices.app.API.v1.db.mongodb.database import users


result = users.find()
for result in result:
    print(result)



def check_mongodb_uri(uri):
    try:
        # Crear una instancia de MongoClient con la URI proporcionada
        client = MongoClient(uri, serverSelectionTimeoutMS=5000)  # 5 segundos de timeout
        
        # Intentar obtener información de la base de datos
        client.admin.command('ping')
        print("Conexión exitosa a MongoDB")
        return client  # Devuelve el cliente si la conexión es exitosa
    except (ServerSelectionTimeoutError, ConfigurationError) as e:
        print(f"Error de conexión: {e}")
        return None  # Devuelve None si hay un error de conexión

def verificar_base_de_datos(client, nombre_db):
    # Listar todas las bases de datos
    bases_de_datos = client.list_database_names()
    print("Bases de datos disponibles:", bases_de_datos)

    # Verificar si la base de datos específica existe
    if nombre_db in bases_de_datos:
        print(f"La base de datos '{nombre_db}' existe.")
        db = client[nombre_db]

        # Listar todas las colecciones en la base de datos
        colecciones = db.list_collection_names()
        print(f"Colecciones en la base de datos '{nombre_db}': {colecciones}")

        return db  # Devuelve la base de datos si existe
    else:
        print(f"La base de datos '{nombre_db}' no existe.")
        return None

# URI de MongoDB
uri = "mongodb://root:example@localhost:27017"

# Nombre de la base de datos a verificar
nombre_db = "PeluqueriaMael"

# Comprobar la URI y obtener el cliente
client = check_mongodb_uri(uri)
if client:
    print("La URI es válida y la conexión se realizó correctamente.")
    
    # Verificar si la base de datos específica existe
    db = verificar_base_de_datos(client, nombre_db)
    
    if db is not None:
        # Acceder a una colección específica (por ejemplo, 'mi_coleccion')
        nombre_coleccion = "Personal"  # Reemplaza 'mi_coleccion' por el nombre de tu colección
        if nombre_coleccion in db.list_collection_names():
            collection = db[nombre_coleccion]
            print(f"La colección '{nombre_coleccion}' existe en la base de datos '{nombre_db}'.")
        else:
            print(f"La colección '{nombre_coleccion}' no existe en la base de datos '{nombre_db}'.")
else:
    print("La URI no es válida o no se pudo conectar a MongoDB.")
