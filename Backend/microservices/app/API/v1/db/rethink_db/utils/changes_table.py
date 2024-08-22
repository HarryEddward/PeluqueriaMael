from Backend.microservices.app.API.v1.db.rethink_db.database import reservas, connection

cursor = reservas.changes().run(connection)

for change in cursor:
    print("Cambio detectado:")
    print(change)