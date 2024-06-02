from fastapi import FastAPI, APIRouter
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi_cache import FastAPICache
from fastapi.middleware.gzip import GZipMiddleware
from fastapi_cache.backends.redis import RedisBackend
from routes.api.main import router as api_router
from routes.apiws.main import router as apiws_router
from routes.cryptoapi.main import router as cryptoapi_router
import ujson
import fastapi
from redis import asyncio as aioredis


fastapi.json = ujson

app = FastAPI()

#Entorno de: prod -> Producción | dev -> Desarrollo 
enviroment = "prod"

@app.on_event("startup")
async def startup_event():

    #Cache for API
    redis = aioredis.from_url("redis://localhost", encoding="utf8", decode_responses=True)
    FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")


# Crear un enrutador base
base_router = APIRouter()


# Incluir los routers específicos en el enrutador base
base_router.include_router(api_router, prefix="/api", tags=["api"])
base_router.include_router(apiws_router, prefix="/apiws", tags=["apiws"])
base_router.include_router(cryptoapi_router, prefix="/cryptoapi", tags=["cryptoapi"])

# Incluir el enrutador base en la aplicación con el prefijo deseado
app.include_router(base_router, prefix="/statusapi/app/api/v1")

app.add_middleware(GZipMiddleware, minimum_size=1000)                   # Solo comprimir respuestas mayores a 1000 bytes
app.add_middleware(                                                     # Configuración del middleware CORS
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Para ejecutar el servidor
if __name__ == "__main__":

    if enviroment == "dev":
        import uvicorn
        uvicorn.run(
            "server:app"
            ,host="localhost"
            ,port=8000
            ,reload=True
            ,workers=2
            ,ssl_certfile='./config/certs/peluqueriamael.com_cert/peluqueriamael.com.crt'
            ,ssl_keyfile='./config/certs/peluqueriamael.com_key.txt'
            
        )
