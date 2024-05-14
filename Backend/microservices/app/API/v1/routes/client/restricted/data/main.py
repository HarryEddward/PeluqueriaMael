from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from db.database import reservas, configure, users, personal as db_personal
from datetime import datetime
from bson import ObjectId
from typing import Optional
from config.config import conf
from datetime import datetime

router = APIRouter(prefix="/data")

from datetime import datetime
import numba as nb

class middleware_struct(BaseModel):
    token_id: Optional[str] = None
    token_data: Optional[str] = None


'''
Porque no se usa el parametro data en las rutas?

- Simplemente es para que se pueda ver las variables a usar en la documentación

'''

@router.post('/appointments')
async def root(request: Request, data: middleware_struct) -> JSONResponse:

    '''
    Enseña las reservas que hizo el **usuario**

    Errores exitentes:
    - DATABASE_ERROR
    - USER_NOT_FOUND
    - UNKNOW_ERROR
    - VERIFY_NOT_TRUE
    '''
    def code() -> dict:

        try:
            user_id = str(request.state.user_id)
            appointments = users.find_one({ "_id": ObjectId(user_id) }, {'_id': 0, 'reservas': 1})
            print('appointments ->', appointments)

        except Exception as e:
            return Response({
                "info": "Hubo un error a la base de datos",
                "status": "no",
                "type": "DATABASE_ERROR"
            }, 401)
        
        if not appointments:
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


@router.post("/services")
async def root(request: Request, data: middleware_struct) -> JSONResponse:

    '''
    Enseña **todos** los **servicios disponibles** dentro de la base de datos

    Errores exitentes:
    - DATABASE_ERROR
    - UNKNOW_ERROR
    '''

    try:

        #@nb.jit(nopython=True)
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
    


class structureBookingDaySheet(BaseModel):
    token_id: Optional[str] = None
    token_data: Optional[str] = None
    day: int
    month: int
    year: int


@router.post('/booking_day_sheet')
async def root(request: Request, data: structureBookingDaySheet) -> JSONResponse:

    '''
    Enseña la **ficha** del usuario

    Errores exitentes:
    - DATABASE_ERROR
    - USER_NOT_FOUND
    - UNKNOW_ERROR
    '''
    def code() -> dict:

        try:
            day = data.day
            month = data.month
            year = data.year

            date_of_the_sheet = datetime(year, month, day)
            appointment_sheet = reservas.find_one({ "fecha": {"$eq": date_of_the_sheet} }, {'_id': 0, 'professionals': 1})
            #print('appointments ->', appointment_sheet)

        except Exception as e:
            return Response({
                "info": f"Hubo un error a la base de datos: {e}",
                "status": "no",
                "type": "DATABASE_ERROR"
            }, 401)
        
        if not appointment_sheet:
            return Response({
                "info": "No se encontro el usuario, o esta en el db vació",
                "status": "no",
                "type": "USER_NOT_FOUND"
            }, 200)


        return Response({
            "info": "Se obtuvo del usuario sus reservas",
            "status": "ok",
            "type": "SUCCESS",
            "data": appointment_sheet
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