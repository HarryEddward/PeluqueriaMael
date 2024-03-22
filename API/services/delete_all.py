from pymongo import MongoClient

# Conectarse al servidor de MongoDB
from API.database import reservas

# Eliminar todos los documentos de la colección
result = reservas.delete_many({})

print(f'Se eliminaron {result.deleted_count} documentos de la colección.')
