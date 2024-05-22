from pymongo import (
    MongoClient
)


client = MongoClient("localhost", 27017)



db = client["PeluqueriaMael"]


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

reservas = db["Reservas"]
users = db["Users"]
configure = db["Configure"]
personal = db["Personal"]
admin = db["Admin"]
types = db["Types"]