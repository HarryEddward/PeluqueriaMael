from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from db.database import reservas, configure, users, personal as db_personal
from datetime import datetime
from bson import ObjectId
from typing import Optional
from config.config import conf

router = APIRouter(prefix="/data")

from datetime import datetime


class middleware_struct(BaseModel):
    token_id: Optional[str] = None
    token_data: Optional[str] = None


@router.post("/services")
async def root(request: Request, data: middleware_struct):

    '''
    Enseña **todos** los **servicios disponibles** dentro de la base de datos
    '''

    try:
        def Response(res: dict, status: int) -> JSONResponse:
            res["renew"] = {"token": request.state.new_token}
            return JSONResponse(res, status)
        try:
            print('config db->', conf["db"]["services"])
            services = configure.find_one({ "_id": ObjectId(conf["db"]["services"]) })

        except Exception as e:
            return Response({
                "info": "Error al obtener los servicios de la base de datos",
                "status": "no",
                "type": "DATABASE_ERROR"
            }, 500)
        
        if not services:
            return Response({
                "info": "No se encuentra ningún documento sobre los servicios",
                "status": "no",
                "type": "DATABASE_ERROR"
            }, 500)

        services.pop('_id', None)

        return Response({
            "info": "Entrega de los servicios de forma correcta",
            "status": "ok",
            "type": "SUCCESS",
            "data": services
        }, 200)

    except Exception as e:
        return JSONResponse({
            "info": f"Error desconocido por el servidor: {e}",
            "status": "no",
            "type": "UNKNOW_ERROR",
            "renew": {
                "token": request.state.new_token
            }
        }, 500)