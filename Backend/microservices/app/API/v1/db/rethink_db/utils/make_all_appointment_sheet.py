from datetime import datetime, timedelta
from pymongo import DESCENDING
from uuid import uuid4
from Backend.microservices.app.API.v1.db.mongodb.database import reservas, personal
from Backend.microservices.app.API.v1.db.rethink_db.database import reservas, connection

# Esquema de disponibilidad para los próximos 120 días
num_days_ahead = 122
start_date = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
dates = [(start_date + timedelta(days=i)).isoformat() for i in range(num_days_ahead)]

'''#print(dates)

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
'''
print(start_date.isoformat())

latest_personal: dict = personal.find_one(sort=[('_id', DESCENDING)])
test_json: dict = {}
test_json["professionals"] = {}
json_professionals: dict = test_json["professionals"]

for types_personal in latest_personal["personal"].keys():
    json_professionals[types_personal] = {}

for profesional, staff in latest_personal["personal"].items():

    for person in staff:
        json_professionals[profesional][person] = {}

test_json["version"] = latest_personal["version"]
#test_json["fecha"]: datetime = start_date.isoformat()

#reservas.insert(test_json).run(connection)

fecha_iso: datetime.isoformat = datetime(2024, 8, 20).isoformat()
count_repeted_sheets = reservas.filter({"fecha": fecha_iso}).count().run(connection)

print(count_repeted_sheets == 0)

for date in dates:
    count_repeted_sheets = reservas.filter({"fecha": date}).count().run(connection)

    if count_repeted_sheets == 0:

        test_json["fecha"]: datetime = date
        reservas.insert(test_json).run(connection)
        print(f"New {date}")
    else:
        print(f"Repeated: {date}, Count: {count_repeted_sheets}")

'''fecha_iso: datetime.isoformat = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0).isoformat()
new_data: dict = {
    "greeting.hello": "it works"
}
reservas.filter({"fecha": fecha_iso}).update(new_data).run(connection)
count_repeted_sheets = reservas.filter({"fecha": fecha_iso}).count().run(connection)
'''
print(f"\n{test_json}\n")


print(dates)