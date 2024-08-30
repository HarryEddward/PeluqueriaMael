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
from Backend.microservices.app.conversor.config.config import Config



'''
IMPORTANTE!

Aplicar en la documentación con Shields.io el status de los
diferentes API en GitHub en la Documentación, y próximamente
en la app del admin.

'''


fastapi.json = ujson


config = Config()

host =      config['host']

ssl_cert =  config['ssl']['cert']
ssl_key =   config['ssl']['key']

app =       config['app']
ssl =       app['StatusAPI']['ssl']
cache =     app['StatusAPI']['cache']
cors =      app["StatusAPI"]["cors"]

port =      app['StatusAPI']['net']['port']



app = FastAPI()

#Entorno de: prod -> Producción | dev -> Desarrollo 
enviroment = "dev"


# Crear un enrutador base
base_router = APIRouter()


@app.on_event("startup")
async def startup_event():

    if cache:
        #Cache for API
        redis = aioredis.from_url(f"redis://{host}", encoding="utf8", decode_responses=True)
        FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")
        print(f'-> REDIS: redis://{host}')
    else:
        print('NO SE ACTIVO EL CACHÉ')



# Incluir los routers específicos en el enrutador base
base_router.include_router(api_router, prefix="/api", tags=["api"])
base_router.include_router(apiws_router, prefix="/apiws", tags=["apiws"])
base_router.include_router(cryptoapi_router, prefix="/cryptoapi", tags=["cryptoapi"])

# Incluir el enrutador base en la aplicación con el prefijo deseado
app.include_router(base_router, prefix="/statusapi/app/api/v1")

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


from middlewares.handleError import ErrorMiddleware
app.add_middleware(ErrorMiddleware)


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