from fastapi import FastAPI, APIRouter
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi_cache import FastAPICache
from fastapi.middleware.gzip import GZipMiddleware
from fastapi_cache.backends.redis import RedisBackend
from routes.admin.admin import router as admin_router
from routes.client.main import router as client_router
from routes.worker.worker import router as worker_router
#from starlette.middleware.sessions import SessionMiddleware
import ujson
import os
import fastapi
from redis import asyncio as aioredis
from Backend.microservices.conversor.config.config import Config

"""
Hola que tal?
"""

config = Config()
host = config['host']

ssl_cert = config['ssl']['cert']
ssl_key = config['ssl']['key']

app = config['app']
ssl = app['API']['ssl']
cache = app['API']['cache']
cors = app["API"]["cors"]
gzip = app["API"]["gzip"]

port = app['API']['net']['port']


fastapi.json = ujson

app = FastAPI()

#Entorno de: prod -> Producción | dev -> Desarrollo 
enviroment = "dev"

@app.on_event("startup")
async def startup_event():

    if cache:
        #Cache for API
        redis = aioredis.from_url(f"redis://{host}", encoding="utf8", decode_responses=True)
        FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")
        print(f'-> REDIS: redis://{host}')
    else:
        print('NO SE ACTIVO EL CACHÉ')

@app.get("/error")
async def trigger_error():
    raise ValueError("This is an Error")

@app.get("/hidden_egg")
def Hidden_Egg() -> HTMLResponse:
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
base_router.include_router(admin_router, prefix="/admin", tags=["admin"])
base_router.include_router(client_router, prefix="/client", tags=["client"])
base_router.include_router(worker_router, prefix="/worker", tags=["worker"])

# Incluir el enrutador base en la aplicación con el prefijo deseado
app.include_router(base_router, prefix="/api/app/api/v1")

#Middlewares
from config.middlewares.client.restricted import RestrictedMiddleware
app.add_middleware(RestrictedMiddleware)

from config.middlewares.client.handleError import ErrorMiddleware
app.add_middleware(ErrorMiddleware)

#app.add_middleware(SessionMiddleware, secret_key="your-secret-key")


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