from datetime import datetime, timedelta
import pymongo

# Conexión a MongoDB
client = pymongo.MongoClient("localhost", 27017)

db = client["PeluqueriaMael"]
collection = db["Reservas"]

# Esquema de disponibilidad para los próximos 120 días
num_days_ahead = 120
start_date = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
dates = [start_date + timedelta(days=i) for i in range(num_days_ahead)]

professionals = {
    "professionals": {
        'peluquero_1': {
            "morning": {
                f"{hour:02d}:{minute:02d}": {"status": "libre"} for hour in range(9, 14) for minute in (0, 30)
            },
            "afternoon": {
                f"{hour:02d}:{minute:02d}": {"status": "libre"} for hour in range(15, 20) for minute in (0, 30)
            }
        },
        'peluquero_2': {
            "morning": {
                f"{hour:02d}:{minute:02d}": {"status": "libre"} for hour in range(9, 14) for minute in (0, 30)
            },
            "afternoon": {
                f"{hour:02d}:{minute:02d}": {"status": "libre"} for hour in range(15, 20) for minute in (0, 30)
            }
        },
        'barbero': {
            "morning": {
                f"{hour:02d}:{minute:02d}": {"status": "libre"} for hour in range(9, 14) for minute in (0, 30)
            },
            "afternoon": {
                f"{hour:02d}:{minute:02d}": {"status": "libre"} for hour in range(15, 20) for minute in (0, 30)
            }
        },
        'esteticista': {
            "morning": {
                f"{hour:02d}:{minute:02d}": {"status": "libre"} for hour in range(9, 14) for minute in (0, 30)
            },
            "afternoon": {
                f"{hour:02d}:{minute:02d}": {"status": "libre"} for hour in range(15, 20) for minute in (0, 30)
            }
        },
    },
    "version": "v2"
}
# Insertar disponibilidad en la base de datos
for date in dates:
    for professional, schedule in professionals.items():
        availability_document = {
            "fecha": date,
            "professionals": schedule
        }
        collection.insert_one(availability_document)

print("Disponibilidad generada y almacenada en la base de datos.")
