import pymongo

# Conecta a tu base de datos (asegúrate de tener el servidor MongoDB en ejecución)
cliente = pymongo.MongoClient('localhost', 27017)

# Selecciona la base de datos
base_de_datos = cliente["PeluqueriaMael"]

# Selecciona la colección
coleccion_reservas = base_de_datos["Users"]

# Realiza la consulta para obtener todos los documentos
todas_las_reservas = coleccion_reservas.find_one({ 'usuario': 'Adrian' })

# Itera sobre los resultados e imprímelos (o realiza cualquier otra operación que necesites)
print(todas_las_reservas)