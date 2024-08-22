#RETHINKDB STRUCTURE DATABASE!

from Backend.microservices.app.API.v1.db.rethink_db.database import (
    server
    ,r
    ,db_name
    ,db
)
from Backend.microservices.conversor.config.config import Config

config = Config()
list_tables = config['db']['persistant']['rethinkdb']['tables']

# Crear la base de datos principal si no existe
try:
    r.db_create(db_name).run(server)
    print('Base de datos test_db creada.')
except r.errors.ReqlOpFailedError:
    print(f'La base de datos {db_name} ya existe.')


for ref, table in list_tables.items():
    table = str(table)
    try:
        r.table_create(table).run(db)
        print(f'Tabla {table} creada.')
    except r.errors.ReqlOpFailedError:
        print(f'La tabla {table} ya existe.')