from pymongo import MongoClient
from datetime import datetime, timedelta

# Conéctate a la base de datos MongoDB
client = MongoClient('localhost', 27017)  # Ajusta la conexión según tu configuración
db = client['PeluqueriaMael']
coleccion_disponibilidad = db['Reservas']

# Obtén la fecha actual
fecha_actual = datetime.now()

# Calcula la fecha más antigua a mantener (hace 90 días)
fecha_mas_antigua = fecha_actual - timedelta(days=1)

# Elimina el día más antiguo
print(fecha_mas_antigua)
coleccion_disponibilidad.delete_one({"fecha": fecha_mas_antigua})

# Calcula la fecha del nuevo día
nueva_fecha = fecha_actual

# Crea la disponibilidad para el nuevo día (puedes ajustar esto según tu estructura)
nueva_disponibilidad = {
    'peluquero_1': {
        "morning": {
            f"{hour:02d}": "libre" for hour in range(9, 14) for minute in (0, 30)
        },
        "afternoon": {
            f"{hour:02d}": "libre" for hour in range(15, 21) for minute in (0, 30)
        }
    },
    'peluquero_2': {
        "morning": {
            f"{hour:02d}": "libre" for hour in range(9, 14) for minute in (0, 30)
        },
        "afternoon": {
            f"{hour:02d}": "libre" for hour in range(15, 21) for minute in (0, 30)
        }
    },
    'barbero': {
        "morning": {
            f"{hour:02d}": "libre" for hour in range(9, 14) for minute in (0, 30)
        },
        "afternoon": {
            f"{hour:02d}": "libre" for hour in range(15, 21) for minute in (0, 30)
        }
    },
    'esteticista': {
        "morning": {
            f"{hour:02d}": "libre" for hour in range(9, 14) for minute in (0, 30)
        },
        "afternoon": {
            f"{hour:02d}": "libre" for hour in range(15, 21) for minute in (0, 30)
        }

}
    # Ajusta según tus profesionales y su disponibilidad
}

# Inserta el nuevo día en la colección
coleccion_disponibilidad.insert_one({"fecha": nueva_fecha, "profesionales": nueva_disponibilidad})

# Cierra la conexión a la base de datos
client.close()
