from pymongo import (
    MongoClient
)
from Backend.microservices.conversor.config.config import Config

config = Config()
db_config = config['db']['persistant']['mongodb']
port = db_config['port']
host = db_config['host']
use_db = db_config['db']
collection = db_config['collections']

use_reservas = collection['reservas']
use_usuarios = collection['usuarios']
use_configuracion = collection['configuracion']
use_personal = collection['personal']
use_administrador = collection['administrador']
use_tipos_de_pydantic = collection['tipos_de_pydantic']


client = MongoClient(host, port)
db = client[use_db]


# Definir los roles para el nuevo usuario
roles = [{"role": "readWrite", "db": "PeluqueriaMael"}]

# Crear el nuevo usuario
'''
db.command(
    'createUser', 'maelsilvero',
    pwd='AXGRbLjzQsMChDnJWdUpNr#87',
    roles=roles
)
'''

reservas = db[use_reservas]
users = db[use_usuarios]
configure = db[use_configuracion]
personal = db[use_personal]
admin = db[use_administrador]
types = db[use_tipos_de_pydantic]