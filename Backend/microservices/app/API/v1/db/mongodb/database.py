import os
from pymongo import (
    MongoClient
)
from Backend.microservices.conversor.config.config import Config

try:
    config: dict = Config()
    db_config: str = config['db']['persistant']['mongodb']
    port: str = db_config['port']
    host: str = db_config['host']
    username: str = db_config['username']
    password: str = db_config['password']
    use_db: str = db_config['db']
    collection: str = db_config['collections']

    use_reservas: str = collection['reservas']
    use_usuarios: str = collection['usuarios']
    use_configuracion: str = collection['configuracion']
    use_personal: str = collection['personal']
    use_administrador: str = collection['administrador']
    use_tipos_de_pydantic: str = collection['tipos_de_pydantic']


    username: str = os.getenv(username)
    password: str = os.getenv(password)

    if (username and password) == None:
        raise "The variables from the enviroment have not configurated yet"

    client: function = MongoClient(f'mongodb://{username}:{password}%s@{host}:{port}')
    db = client[use_db]


    # Crear el nuevo usuario
    '''
    db.command(
        'createUser', 'ddsfsdf',
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
except Exception as err:
    raise f"Have a problem in database.py from API: {err}"