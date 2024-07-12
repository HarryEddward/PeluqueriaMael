import pymongo

# Conectarse a la base de datos de MongoDB
cliente = pymongo.MongoClient("mongodb://localhost:27017/")
base_datos = cliente["PeluqueriaMael"]
coleccion = base_datos["Users"]

# Datos del nuevo usuario
nuevo_usuario = {
    "usuario": "Adrian",
    "contraseña": "12324324234"
}

# Añadir el nuevo usuario a la colección
coleccion.insert_one(nuevo_usuario)

print("Usuario añadido exitosamente.")
