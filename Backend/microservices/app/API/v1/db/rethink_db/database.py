import rethinkdb as r
from Backend.microservices.conversor.config.config import Config

config = Config()

config_db = config['db']['persistant']['rethinkdb']
port = config_db['port']['client']
host = config_db['host']

reservas = config_db["tables"]["reservas"]

db_name = config_db['db']

try:
    # Conectarse a RethinkDB
    r = r.r
    connection = r.connect(host=host, port=port, db=db_name)
    reservas = r.db(db_name).table(reservas)

    documents = reservas.run(connection)

except Exception as e:

    print(f"Hay un buen problema con RethinkDB: {e}")