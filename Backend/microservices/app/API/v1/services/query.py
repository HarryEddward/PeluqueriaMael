from datetime import datetime

from Backend.microservices.app.API.v1.db.mongodb.database import reservas

# Fecha de Python para comparar
fecha_python = datetime(2024, 3, 15)
print(fecha_python)

# Realizar la consulta en MongoDB
resultados = reservas.find({"fecha": {"$eq": fecha_python}})

# Iterar sobre los resultados
for documento in resultados:
    print(documento)


