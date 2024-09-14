from fastapi import APIRouter, Request, Response
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from Backend.microservices.app.API.v1.db.mongodb.database import reservas, configure, users, personal as db_personal
from datetime import datetime
from bson import ObjectId
from typing import Optional
from config.config import conf
from crud.mongodb.client.users.delete import UserDelete
from Backend.microservices.app.API.v1.db.redis_db.database import rate_limit

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


@router.options('/delete')
async def User_Delete_Options(response: Response):

    response.headers["Allow"] = "POST, OPTIONS"
    response.headers["Content-Type"] = "application/json"
    return {
        "options": ["POST", "OPTIONS"]
    }


@router.post('/delete')
@rate_limit("5/10s")
async def User_Delete(request: Request, data: structureDelete) -> JSONResponse:

    '''
    Ruta para **eliminar** la cuenta del **usuario existente**


    Errores exitentes:
    - DATABASE_ERROR
    - USER_NOT_FOUND
    - UNKNOW_ERROR
    - APPOINTMENTS_EXISTENTS
    '''
    def code() -> dict:
        
        verify = data.verify
        print(request.state.new_token)

        # Si la eliminación de la cuenta no esta verificada, no se puede eliminar. Puede ser que manera no intencionada
        if not verify:
            return {
                "info": "No quiso eliminar la cuenta de forma intenconada",
                "status": "no",
                "type": "VERIFY_NOT_TRUE"
            }

        try:
            user_id = str(request.state.user_id)
            user = users.find_one({ "_id": ObjectId(user_id) }, { '_id': 0 })

        except Exception as e:
            return Response({
                "info": "Hubo un error a la base de datos",
                "status": "no",
                "type": "DATABASE_ERROR"
            }, 401)
        
        #Elimina la cuenta del usuario
        delete_user = UserDelete(
            UserDelete.structure(
                user_id=user_id
            )
        )
        
        #print('Delete User->', delete_user.response)
        if not delete_user.response["status"] == 'ok':
            return Response(delete_user.response, 401)

        #print('sus ->', print)
        return Response({
            "info": "Se obtuvo del usuario sus reservas",
            "status": "ok",
            "type": "SUCCESS"
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

