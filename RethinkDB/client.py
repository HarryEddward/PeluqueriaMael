from rethinkdb import RethinkDB
from rethinkdb.errors import RqlRuntimeError, RqlDriverError

r = RethinkDB()

# Conectar a la base de datos
rdb_conn = r.connect("localhost", 28015).repl()

# Crear una base de datos y una tabla si no existen
try:
    r.db_create('test').run(rdb_conn)
except RqlRuntimeError:
    pass  # La base de datos ya existe

try:
    r.db('test').table_create('authors').run(rdb_conn)
except RqlRuntimeError:
    pass  # La tabla ya existe

def monitor_changes():
    try:
        feed = r.db('test').table('authors').changes().run(rdb_conn)
        print("Monitoring changes on 'authors' table...")
        for change in feed:
            print("Change detected:", change)
    except RqlRuntimeError as e:
        print("Error: ", e)

if __name__ == "__main__":
    monitor_changes()
