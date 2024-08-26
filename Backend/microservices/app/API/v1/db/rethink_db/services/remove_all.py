from typing import Any, Dict
from Backend.microservices.app.API.v1.db.rethink_db.database import reservas, connection

try:
    # Eliminar todos los documentos de la tabla
    result = reservas.delete().run(connection)
    print(f"Documentos eliminados: {result['deleted']}")

except Exception as e:
    print(f"Error al eliminar documentos: {e}")