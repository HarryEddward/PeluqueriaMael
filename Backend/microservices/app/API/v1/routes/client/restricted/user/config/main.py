from fastapi import APIRouter, Request, Response
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from Backend.microservices.app.API.v1.db.mongodb.database import reservas, configure, users, personal as db_personal
from datetime import datetime
from bson import ObjectId
from typing import Optional
from config.config import conf

router = APIRouter(prefix="/config")

from datetime import datetime
import numba as nb


'''
Porque no se usa el parametro data en las rutas?

- Simplemente es para que se pueda ver las variables a usar en la documentación

'''


class structureResetPassword(BaseModel):
    token_id: Optional[str] = None
    token_data: Optional[str] = None
    current_psw: str
    new_psw: str

@router.options('/reset_password')
async def Config_Reset_Password_Options(response: Response):

    response.headers["Allow"] = "POST, OPTIONS"
    response.headers["Content-Type"] = "application/json"
    return {
        "options": ["POST", "OPTIONS"]
    }

@router.post('/reset_password')
async def Config_Reset_Password(request: Request, data: structureResetPassword) -> JSONResponse:

    '''
    La ruta **cambia** la contraseña actual **por la nueva** del usuario
    '''
    def code() -> dict:

        current_psw = str(data.current_psw)
        new_psw = str(data.new_psw)

        try:
            #print('--------------------')
            user_id = str(request.state.user_id)

            #Obtiene la contraseña sin ser procesado
            current_psw_db_raw = users.find_one({ "_id": ObjectId(user_id) }, {'_id': 0, 'data.info.password': 1})
            
            #Obtiene la contraseña procesado
            current_psw_db = current_psw_db_raw["data"]["info"]["password"]
            #print('appointments ->', current_psw)

        except Exception as e:
            return Response({
                "info": "Hubo un error a la base de datos",
                "status": "no",
                "type": "DATABASE_ERROR"
            }, 401)
        
        if not current_psw_db:
            return Response({
                "info": "No se encontro el usuario, o esta en el db vació",
                "status": "no",
                "type": "USER_NOT_FOUND"
            }, 401)
        
        #print('current_psw ->', current_psw)
        #print('new_psw ->', new_psw)
        #print('current_psw_db ->', current_psw_db)
        

        
        # Valida si la contraseña puesta "actual" es el mismo que la contraseña actual en el db
        if not current_psw_db == current_psw:

            print('No cuadra la contraseña con el db')
            return Response({
                "info": "La contraseña no cuadra con la actual",
                "status": "no",
                "type": "PASSWORD_DONT_MATCH"
            }, 401)
        
        print('--------------------')
        
        #Cambia la contraseña si todo fué bien
        try:
            users.update_one(
                {"_id": ObjectId(user_id)},
                { "$set": {
                        "data.info.password": new_psw
                    }
                }
            )
        except Exception as e:
            return Response({
                "info": "Hubo un error a la base de datos",
                "status": "no",
                "type": "DATABASE_ERROR"
            }, 401)

        return Response({
            "info": "Se cambio la contraseña actual por la nueva contraseña",
            "status": "ok",
            "type": "SUCCESS",
            "data": new_psw
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


