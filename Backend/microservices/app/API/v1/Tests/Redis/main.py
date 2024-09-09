from Backend.microservices.app.API.v1.db.redis_db.database import RedisClient
import asyncio
import time
# Cambia esto a la ruta correcta de tu archivo RedisClient

async def simple_redis_set():
    # Conectar a Redis
    await RedisClient.connect()
    
    # Obtener el cliente Redis
    client = RedisClient.get_client()
    
    # Establecer clave-valor
    await client.setex("mi_clave", 120, "mi_valor")
    time.sleep(10)

    # Obtener y mostrar el valor
    valor = await client.get("mi_clave")
    print(f"Valor para 'mi_clave': {type(valor)}")
    
    time.sleep(120)
    valor = await client.get("mi_clave")
    print(f"Valor para 'mi_clave': {type(valor)}")


    # Desconectar de Redis
    await RedisClient.disconnect()

# Ejecutar la función
if __name__ == "__main__":
    asyncio.run(simple_redis_set())
