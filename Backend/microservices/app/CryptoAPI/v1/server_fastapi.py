from fastapi import FastAPI, APIRouter
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi_cache import FastAPICache
from fastapi.middleware.gzip import GZipMiddleware
from fastapi_cache.backends.redis import RedisBackend
from Backend.microservices.app.CryptoAPI.v1.routes.cpu.main import router as cpu_router
from Backend.microservices.app.CryptoAPI.v1.routes.gpu.main import router as gpu_router
#from starlette.middleware.sessions import SessionMiddleware
import ujson
import os
import fastapi
import logging
from redis import asyncio as aioredis
from Backend.microservices.conversor.config.config import Config

logging.basicConfig(filename="app.log", level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

config: dict = Config()
host: str = config['host']

ssl_cert: str = config['ssl']['cert']
ssl_key: str = config['ssl']['key']

app: str = config['app']
ssl: str = app['CryptoAPI']['ssl']
cache: str = app['CryptoAPI']['cache']
cors: str = app["CryptoAPI"]["cors"]
gzip: str = app["CryptoAPI"]["gzip"]

port: str = app['CryptoAPI']['net']['port']
cpu: str = app['CryptoAPI']['cpu']
gpu: str = app['CryptoAPI']['gpu']['enabled']


fastapi.json = ujson

app = FastAPI()

#Entorno de: prod -> Producción | dev -> Desarrollo 
enviroment = "dev"

@app.on_event("startup")
async def startup_event():

    if cache:
        #Cache for API
        redis: str = aioredis.from_url(f"redis://{host}", encoding="utf8", decode_responses=True)
        FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")
        print(f'-> REDIS: redis://{host}')
    else:
        print('NO SE ACTIVO EL CACHÉ')

@app.get("/hidden_egg")
def read_root():
    return HTMLResponse(
        content="""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Hidden egg</title>
        </head>
        <body>
            <img src="https://images.pexels.com/photos/3343/easter-eggs.jpg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=0">
        </body>
        </html>
        """, 
        status_code=200)

# Crear un enrutador base
base_router = APIRouter()


# Incluir los routers específicos en el enrutador base

if cpu:
    print('ADD CPU')
    base_router.include_router(cpu_router, prefix="/cpu", tags=["cpu"])
if gpu:
    print('ADD GPU')
    base_router.include_router(gpu_router, prefix="/gpu", tags=["gpu"])


# Incluir el enrutador base en la aplicación con el prefijo deseado
app.include_router(base_router, prefix="/cryptoapi/app/api/v1")



# Middlewares
#app.add_middleware(SessionMiddleware, secret_key="your-secret-key-3")
#Comprueba si es texto en plano, no va a comprobar mas que simple texto

from Backend.microservices.app.CryptoAPI.v1.middlewares.octet_stream import OctetStreamMiddleware

# Rutas que el middleware debe omitir
skip_paths: list = ["/docs", "/redoc", "/openapi"]

# Agregar el middleware a la aplicación y pasar las rutas a omitir
app.add_middleware(OctetStreamMiddleware, skip_paths=skip_paths)

from middlewares.handleError import ErrorMiddleware
app.add_middleware(ErrorMiddleware)


'''
Si gzip esta activado del archivo de configuración lo añade el middleware!
'''
if gzip['enabled']:
    app.add_middleware(GZipMiddleware, minimum_size=gzip['min_size'])                   # Solo comprimir respuestas mayores a 1000 bytes

'''
Si cors esta activado del archivo de configuración lo añade el middleware!
'''
if cors['enabled']:
    app.add_middleware(                                                     # Configuración del middleware CORS
        CORSMiddleware,
        allow_origins=cors["origins"],  
        allow_credentials=True,
        allow_methods=cors["methods"],
        allow_headers=cors["headers"],
    )

# Para ejecutar el servidor
if __name__ == "__main__":

    if enviroment == "dev":
        import uvicorn

        if ssl:
            uvicorn.run(
                "server_fastapi:app"
                ,host=host
                ,port=port
                ,reload=True
                ,workers=2
                ,ssl_certfile=ssl_cert
                ,ssl_keyfile=ssl_key   
            )
        else :
            uvicorn.run(
                "server_fastapi:app"
                ,host=host
                ,port=port
                ,reload=True
                ,workers=2
            )