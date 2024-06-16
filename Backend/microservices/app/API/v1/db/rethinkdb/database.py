import rethinkdb as r
from Backend.microservices.conversor.config.config import Config

config = Config()

config_db = config['db']['persistant']['rethinkdb']
port = config_db['port']['client']
host = config_db['host']

db_name = config_db['db']

# Conectarse a RethinkDB
r = r.r

server = r.connect(host=host, port=port)
db = r.connect(host=host, port=port, db=db_name)