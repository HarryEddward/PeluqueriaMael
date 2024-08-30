from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes.app.admin import admin
from routes.app.client import client
from routes.app.worker import worker
from routes.public import public

import os

app = FastAPI()


# Incluyendo los routers
app.include_router(admin.router, prefix="/app/admin", tags=["admin"])
app.include_router(client.router, prefix="/app/worker", tags=["worker"])
app.include_router(worker.router, prefix="/app/client", tags=["client"])
app.include_router(public.router, prefix="/public", tags=["public"])

# Configuración del middleware CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["192.168.1.135"],  # O puedes especificar dominios permitidos
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

from middlewares.handleError import ErrorMiddleware
app.add_middleware(ErrorMiddleware)


@app.get("/")
def read_root():
    return {"message": "¡Bienvenido a mi servidor FastAPI!"}

'''
#Dev Section

if __name__ == "__main__":
    import uvicorn
    uvicorn.run('server:app', host="0.0.0.0", port=8000, reload=True, workers=2)
'''