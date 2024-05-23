from rethinkdb import RethinkDB
from tornado import ioloop, gen

r = RethinkDB()

r.set_loop_type("tornado")


@gen.coroutine
def connect_to_db():
    conn = yield r.connect(host="localhost", port=28015)
    return conn

db_connection = ioloop.IOLoop.current().run_sync(connect_to_db)
