from pymongo import MongoClient
import os

host = "localhost"  # Nombre del servicio
port = 27017

connection_uri = f'mongodb://{host}:{port}'

try:
    client = MongoClient(connection_uri, serverSelectionTimeoutMS=5000)  # Timeout de 5 segundos
    client.admin.command('ping')  # Verifica la conexión con un ping
    print("Conexión exitosa a MongoDB")
except Exception as e:
    print(f"No se pudo conectar a MongoDB: {e}")
