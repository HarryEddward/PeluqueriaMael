import os
from pymongo import MongoClient
from urllib.parse import quote_plus
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

    # Codifica el nombre de usuario y la contraseña
    username = quote_plus(username)
    password = quote_plus(password)

    # Verifica las variables de entorno
    username_env = os.getenv('USERNAME_ENV')  # Ajusta si el nombre de variable es diferente
    password_env = os.getenv('PASSWORD_ENV')  # Ajusta si el nombre de variable es diferente

    if username_env:
        username = username_env
    if password_env:
        password = password_env

    if not (username and password):
        raise ValueError("The variables from the environment have not been configured yet")

    # Construye la URL de conexión
    connection_uri = f'mongodb://{username}:{password}@{host}:{port}/{use_db}'
    client = MongoClient(connection_uri)
    db = client[use_db]

    reservas = db[use_reservas]
    users = db[use_usuarios]
    configure = db[use_configuracion]
    personal = db[use_personal]
    admin = db[use_administrador]
    types = db[use_tipos_de_pydantic]
except Exception as err:
    print(err)
    raise RuntimeError(f"Have a problem in database.py from API: {err}")
