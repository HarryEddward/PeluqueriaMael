from fastapi import FastAPI
from API.routes.app import admin, client, worker
from routes.app import (
    admin,
    worker,
    client
)
from routes import public
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()

app.include_router(admin.router, prefix="/app/admin", tags=["admin"])
app.include_router(worker.router, prefix="/app/worker", tags=["worker"])
app.include_router(client.router, prefix="/app/client", tags=["client"])
app.include_router(public.router, prefix="/public", tags=["public"])


app.add_middleware(
    CORSMiddleware,
    allow_origins=["192.168.1.135"],  # O puedes especificar dominios permitidos
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



@app.get("/")
def read_root():
    return {"message": "¡Bienvenido a mi servidor FastAPI!"}
