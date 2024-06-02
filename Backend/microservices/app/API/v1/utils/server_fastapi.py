from fastapi import FastAPI, APIRouter
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi_cache import FastAPICache
from fastapi.middleware.gzip import GZipMiddleware
from fastapi_cache.backends.redis import RedisBackend
from routes.admin.admin import router as admin_router
from routes.client.main import router as client_router
from routes.worker.worker import router as worker_router
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
base_router.include_router(admin_router, prefix="/admin", tags=["admin"])
base_router.include_router(client_router, prefix="/client", tags=["client"])
base_router.include_router(worker_router, prefix="/worker", tags=["worker"])

# Incluir el enrutador base en la aplicación con el prefijo deseado
app.include_router(base_router, prefix="/api/app/api/v1")

#Middlewares
from config.middlewares.client.restricted import RestrictedMiddleware
app.add_middleware(RestrictedMiddleware)                                #/app/api/v1/client/restricted/
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
