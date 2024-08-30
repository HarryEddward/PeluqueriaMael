import aioredis
from fastapi import FastAPI
from redis.asyncio import Redis
from typing import Optional
from abc import ABC, abstractmethod

class Verify(ABC):

    _client: Optional[Redis]

    @abstractmethod
    async def connect(cls, redis_url: str):
        pass

    @abstractmethod
    async def disconnect(cls):
        pass
    
    @abstractmethod
    async def get_client(cls) -> Optional[Redis]:
        pass

    @abstractmethod
    async def set_cache(cls, key: str, value: str, expire: int):
        pass

    @abstractmethod
    async def get_cache(cls, key: str) -> Optional[str]:
        pass


class RedisClient(Verify):
    _client: Optional[Redis] = None

    @classmethod
    async def connect(cls, redis_url: str):
        try:
            cls._client = Redis.from_url(redis_url, encoding="utf-8", decode_responses=True)
            await cls._client.ping()  # Verificar la conexión
            print("Conexión a Redis establecida.")
        except Exception as e:
            cls._client = None
            print(f"Error al conectar a Redis: {e}")

    @classmethod
    async def disconnect(cls):
        if cls._client:
            await cls._client.close()
            print("Conexión a Redis cerrada.")

    @classmethod
    def get_client(cls) -> Optional[Redis]:
        return cls._client

    @classmethod
    async def set_cache(cls, key: str, value: str, expire: int):
        if cls._client:
            await cls._client.set(key, value, ex=expire)

    @classmethod
    async def get_cache(cls, key: str) -> Optional[str]:
        if cls._client:
            return await cls._client.get(key)
        return None

# Middleware para verificar la conexión a Redis al iniciar FastAPI
async def check_redis_connection():
    client = RedisClient.get_client()
    if not client:
        print("Redis no está conectado. Verifica la configuración.")
    else:
        print("Redis está conectado correctamente.")
