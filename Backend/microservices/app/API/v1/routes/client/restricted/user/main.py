from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from db.database import reservas, configure, users, personal as db_personal
from datetime import datetime
from bson import ObjectId
from typing import Optional
from config.config import conf


'''
En esta ruta solamnete es operaciónes internas del usaurio y no cambios en si.
Como por ejemplo eliminar la cuenta, operaciónes englobadas con el usuario, no en cambios de configruación
'''

from .config.main import router as router_config
router = APIRouter(prefix="/user")

router.include_router(router_config)

from datetime import datetime
import numba as nb

class middleware_struct(BaseModel):
    token_id: Optional[str] = None
    token_data: Optional[str] = None


'''
Porque no se usa el parametro data en las rutas?

- Simplemente es para que se pueda ver las variables a usar en la documentación

'''

class structureDelete(BaseModel):
    token_id: Optional[str] = None
    token_data: Optional[str] = None
    verify: bool


@router.post('/delete')
async def root(request: Request, data: structureDelete) -> JSONResponse:

    '''
    Ruta para **eliminar** la cuenta del **usuario existente**


    Errores exitentes:
    - DATABASE_ERROR
    - USER_NOT_FOUND
    - UNKNOW_ERROR
    '''
    def code() -> dict:

        try:
            user_id = str(request.state.user_id)
            user = users.find_one({ "_id": ObjectId(user_id) }, {'_id': 0})

        except Exception as e:
            return Response({
                "info": "Hubo un error a la base de datos",
                "status": "no",
                "type": "DATABASE_ERROR"
            }, 401)
        
        #Verifica si existe el usuario
        if not user:
            return Response({
                "info": "No se encontro el usuario, o esta en el db vació",
                "status": "no",
                "type": "USER_NOT_FOUND"
            }, 200)

        # Convertir objetos datetime a cadenas de texto
        for _, reservas in appointments['reservas'].items():
            print('reservas---->', reservas)
            reservas["date_appointment"] = str(reservas["date_appointment"])

        return Response({
            "info": "Se obtuvo del usuario sus reservas",
            "status": "ok",
            "type": "SUCCESS",
            "data": appointments
        }, 200)



    try:
        def Response(res: dict, status: int) -> JSONResponse:
            res["renew"] = {
                "token": request.state.new_token
            }
            return JSONResponse(res, status)
        
        return code()
        
        

    except Exception as e:
        return JSONResponse({
            "info": f"Error desconocido por el servidor: {e}",
            "status": "no",
            "type": "UNKNOW_ERROR",
            "renew": {
                "token": request.state.new_token
            }
        }, 500)

