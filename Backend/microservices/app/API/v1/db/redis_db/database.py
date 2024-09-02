import asyncio
from typing import Optional
from redis.asyncio import Redis
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from fastapi import FastAPI
from fastapi.responses import JSONResponse
import logging
from abc import ABC, abstractmethod
from Backend.microservices.app.API.v1.logging_config import logger
from Backend.microservices.conversor.config.config import Config

config: dict = Config()
db_config: dict = config["db"]["temporary"]["redis"]
host: str = db_config["host"]
port: int = db_config["port"]
API_db: str = db_config["db"]["microservices"]["app"]["API"]


class Verify(ABC):

    REDIS_URL: str
    _client: Optional[Redis] = None

    @abstractmethod
    async def connect(cls) -> None:
        pass

    @abstractmethod
    async def disconnect(cls) -> None:
        pass

    @abstractmethod
    def get_client(cls) -> Optional[Redis]:
        pass


class RedisClient(Verify):

    # Configuración de Redis
    REDIS_URL: str = f"redis://{host}:{port}/{API_db}"
    
    _client: Optional[Redis] = None

    @classmethod
    async def connect(cls) -> None:
        try:
            cls._client = Redis.from_url(cls.REDIS_URL, encoding="utf-8", decode_responses=True)
            await cls._client.ping()  # Verificar la conexión
            #logger.info(f"Conexión a Redis establecida. URL: {cls.REDIS_URL}")
        except Exception as e:
            cls._client = None
            logger.error(f"Error al conectar a Redis: {e}")

    @classmethod
    async def disconnect(cls) -> None:
        if cls._client:
            await cls._client.close()
            logger.info("Conexión a Redis cerrada.")

    @classmethod
    def get_client(cls) -> Optional[Redis]:
        return cls._client

# Configura y exporta el Limiter
limiter = Limiter(key_func=get_remote_address)

def setup_redis_limiters_and_cache(app: FastAPI):
    redis_client = RedisClient.get_client()
    limiter.storage = redis_client

    FastAPICache.init(RedisBackend(redis_client), prefix="fastapi-cache")

    @app.exception_handler(RateLimitExceeded)
    async def rate_limit_exceeded_handler(request, exc: RateLimitExceeded):
        return JSONResponse(
            status_code=429,
            content={
                "info": "Rate limit exceeded. Please try again later.",
                "status": "no",
                "type": "RATE_LIMIT_ERROR"
            }
        )

    app.state.limiter = limiter

# Exportar el decorador @limiter.limit
rate_limit = limiter.limit

