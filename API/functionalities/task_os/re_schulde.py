from pymongo import MongoClient
from datetime import datetime, timedelta


from API.database import reservas
# Conectarse a la base de datos MongoDB


# Función para verificar la existencia de modelos para los próximos 90 días
def verificar_y_crear_modelos():
    # Obtener la fecha actual
    fecha_actual = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)


    # Obtener las fechas existentes en la colección
    fechas_existentes = set(doc["fecha"] for doc in reservas.find({}, {"fecha": 1}))

    # Iterar sobre los próximos 120 días
    for i in range(120):
        # Calcular la fecha de iteración
        fecha_iteracion = fecha_actual + timedelta(days=i)

        # Verificar si la fecha de iteración ya existe en la colección
        if fecha_iteracion not in fechas_existentes:
            # Si no existe, crear un modelo utilizando la estructura proporcionada
            modelo = {
                "fecha": fecha_iteracion,
                "professionals": {
                    "peluquero_1": {"morning": {}, "afternoon": {}},
                    "peluquero_2": {"morning": {}, "afternoon": {}},
                    "barbero": {"morning": {}, "afternoon": {}},
                    "esteticista": {"morning": {}, "afternoon": {}}
                }
            }
            # Agregar la estructura de horarios con los horarios específicos
            for key in modelo["professionals"].keys():
                for period in ["morning", "afternoon"]:
                    if period == "morning":
                        start_hour = 9
                        end_hour = 13
                    elif period == "afternoon":
                        start_hour = 15
                        end_hour = 19  # Hora final 20:00, pero el último bloque empieza a las 19:30
                    for hour in range(start_hour, end_hour + 1):  # +1 para incluir la hora final
                        for minute in range(0, 60, 30):
                            time_slot = f"{hour:02d}:{minute:02d}"
                            modelo["professionals"][key][period][time_slot] = {"status": "libre"}

            # Insertar el modelo en la colección de reservas
            reservas.insert_one(modelo)

# Llamar a la función para verificar y crear modelos
verificar_y_crear_modelos()

# Imprimir la cantidad de documentos en la colección de reservas
print(f"Total de documentos en la colección 'Reservas': {reservas.count_documents({})}")