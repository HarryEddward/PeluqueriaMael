#PYMONGO STRUCTURE DATABASE!

from Backend.microservices.conversor.config.config import Config
from Backend.microservices.app.API.v1.db.mongodb.database import client

config = Config()
db_config = config['db']['persistant']['mongodb']

use_db = db_config['db']
collection = db_config['collections']


# Verificar si la base de datos ya existe
if use_db in client.list_database_names():
    print(f'La base de datos {use_db} ya existe.')
else:
    # Crear la base de datos
    db = client[use_db]
    print(f'Base de datos {use_db} creada.')

    # Crear las colecciones en la nueva base de datos
    for coleccion in collection.item():
        db.create_collection(coleccion)
        print(f'Colección {coleccion} creada en la base de datos {use_db}.')
        
# Verificar y notificar si las colecciones ya existen
db = client[use_db]  # Seleccionar la base de datos

for ref, coleccion in collection.items():
    if coleccion in db.list_collection_names():
        print(f'La colección {coleccion} ya existe en la base de datos {use_db}.')
    else:
        db.create_collection(coleccion)
        print(f'Colección {coleccion} creada en la base de datos {use_db}.')
