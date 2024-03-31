from pymongo import MongoClient

# Configuración de la conexión a MongoDB
client = MongoClient('mongodb://mongoadmin:bdung@localhost:27018/')
db = client['mydatabase']  # Cambia 'mydatabase' por el nombre de tu base de datos
collection = db['mycollection']  # Cambia 'mycollection' por el nombre de tu colección

# Verificar si la colección existe
if collection.count_documents({}) == 0:
    # La colección no existe, crea una nueva colección y agrega un documento
    collection.insert_one({
        'nombre': 'ejemplo',
        'edad': 30,
        'ciudad': 'ejemplo'
    })
    print("Se creó una nueva colección 'mycollection' y se añadió un documento.")
else:
    # La colección ya existe, no hagas nada
    print("La colección 'mycollection' ya existe, no se creó una nueva colección.")

# Cierra la conexión con MongoDB
client.close()
