from Backend.microservices.app.API.v1.db.rethink_db.database import reservas, connection, documents

cursor_changes = reservas.changes().run(connection)


for doc in documents:
    print(doc)

for change in cursor_changes:
    print("Cambio detectado:")
    print(change)