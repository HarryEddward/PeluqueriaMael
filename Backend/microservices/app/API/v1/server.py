from fastapi import FastAPI, APIRouter
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from routes.admin.admin import router as admin_router
from routes.client.main import router as client_router
from routes.worker.worker import router as worker_router
import ujson
import fastapi

fastapi.json = ujson

app = FastAPI()


@app.get("/hidden_egg")
def read_root():
    return JSONResponse({
        "info": ":o",
        "status": "Shhh",
        "type": "EASTER_EGG"
    }, 200)

# Crear un enrutador base
base_router = APIRouter()

# Incluir los routers específicos en el enrutador base
base_router.include_router(admin_router, prefix="/admin", tags=["admin"])
base_router.include_router(client_router, prefix="/client", tags=["client"])
base_router.include_router(worker_router, prefix="/worker", tags=["worker"])

# Incluir el enrutador base en la aplicación con el prefijo deseado
app.include_router(base_router, prefix="/app/api/v1")

#Middlewares
from config.middlewares.client.restricted import RestrictedMiddleware
app.add_middleware(RestrictedMiddleware) #/app/api/v1/client/restricted/

# Configuración del middleware CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["192.168.1.135"],  # O puedes especificar dominios permitidos
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
'''
# Para ejecutar el servidor
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True, workers=2)
'''