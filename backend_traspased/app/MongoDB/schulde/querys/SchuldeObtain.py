from pymongo import MongoClient
from bson import ObjectId

# Conexión a la base de datos
client = MongoClient('mongodb://localhost:27017/')
db = client["PeluqueriaMael"]
coleccion = db["Reservas"]

# Encuentra los 30 documentos más recientes ordenados por fecha de creación descendente
resultados = coleccion.find().sort('fecha', -1).limit(30)

# Imprime o realiza alguna operación con los resultados
for resultado in resultados:
    print("Fecha:", resultado["fecha"])
    print("_id:", resultado["_id"])


_id = ObjectId('6553feb52668a7f603908884')
resultado = coleccion.find_one({"_id": _id})

print(resultado["fecha"])