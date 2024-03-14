from pymongo import MongoClient
from datetime import datetime

# Establecer la conexión con la base de datos
client = MongoClient('localhost', 27017)
db = client['PeluqueriaMael']
collection = db['Reservas']

# Fecha de Python para comparar
fecha_python = datetime(2024, 3, 15)
print(fecha_python)

# Realizar la consulta en MongoDB
resultados = collection.find({"fecha": {"$eq": fecha_python}})

# Iterar sobre los resultados
for documento in resultados:
    print(documento)


