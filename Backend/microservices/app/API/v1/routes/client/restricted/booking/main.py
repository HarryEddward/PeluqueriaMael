from fastapi import (
    APIRouter,
    Request,
    HTTPException,
    status
)
from fastapi.responses import JSONResponse

from crud.booking.utils.serviceToPersonal import serviceToPersonal
from crud.booking.utils.workerLessBusy import workerLessBusy
from crud.booking.utils.conversorServices import conversorServices
from crud.booking.add import AddBooking
from crud.booking.remove import RemoveBooking

from pydantic import BaseModel
from pydantic import validator
from pydantic import ValidationError

from Backend.microservices.app.API.v1.db.mongodb.database import reservas, configure, users, personal as db_personal
from datetime import datetime

from bson import ObjectId
from typing import Optional
from typing import Literal
from typing import Union
import numba as nb

router = APIRouter(prefix="/booking")



class structure_test(BaseModel):
    day: int
    month: int
    year: int
    service: str

'''
Convertir el token en un simple id que pueda hacerse uso
'''

class structureRemove(BaseModel):
    token_id: Optional[str] = None
    token_data: Optional[str] = None
    id_reserva: str

@router.post("/remove")
async def Remove_Appointment(request: Request, data: structureRemove):

    """
    Ruta para **quitar las reservas** de los **clientes**

    Errores exitentes:
    - DATABASE_ERROR
    - NOT_EXIST_BOOKING_ID
    - UNKNOW_ERROR
    - SERVICE_ERROR
    - VERIFY_DAYS_ERROR
    """


    try:
        #-> Responde de forma añadiendo el jwt integrado
        
        #@nb.jit(nopython=True)
        def Response(res: dict, status: int) -> JSONResponse:
            res["renew"] = {"token": request.state.new_token}
            return JSONResponse(res, status)
        
        #-> Responde de forma añadiendo el jwt integrado


        #-> Obtiene el usuario del id, y la ficha de reserva de ese día
        try:
            user_id: str = request.state.user_id
            id_reserva: str = data.id_reserva
            user = users.find_one(
                { "_id": ObjectId(user_id) },
                {f"data.reservas.{id_reserva}": 1, "_id": 0}
            )
            user = user['data']['reservas']

            print(f'data.reservas.{id_reserva}:', user)
        except Exception as e:
            return Response({
                "info": "Error en la base de datos, quizas no exista y tengas mal los mismos parametros",
                "status": "no",
                "type": "DATABASE_ERROR"
            }, 401)
        
        if id_reserva not in user:
            print('->', id_reserva)
            print('->', id_reserva not in user)
            print('->', user)

            return Response({
                "info": "La id que pasaste no existe dentro del usuario",
                "status": "no",
                "type": "NOT_EXIST_BOOKING_ID"
            }, 401)
    
        reserva = user[id_reserva]
        #-> Obtiene el usuario del id, y la ficha de reserva de ese día


        #-> Parsea las variables para hacerlo úso en la ruta
        day_booked = reserva["date_appointment"].day
        month_booked = reserva["date_appointment"].month
        year_booked = reserva["date_appointment"].year
        period_booked = reserva["period"]
        start_time_booked = reserva["start_time"]
        responsable_appointment_booked = reserva["responsable_appointment"]
        service_booked = reserva["service"]

        print(day_booked, month_booked, year_booked)
        #-> Parsea las variables para hacerlo úso en la ruta


        #-> Obtiene los servicios actuales para reservar
        services = conversorServices()

        print('services ->', services.response)

        if services is not None:
            if not services.response["status"] == 'ok':
                return Response(services.response, 401)
        else:
            return Response({
                "info": "Error al obtener los servicios.",
                "sub_response": services.response,
                "status": "no",
                "type": "SERVICE_ERROR"
            }, 401)

        services = services.response["data"]
        #-> Obtiene los servicios actuales

        
        #-> Verifica que si faltan 3 dias
        '''/crud/booking/utils/remove/verify_days.py'''
        from crud.booking.utils.remove.verifyDays import verifyDays

        verify_days = verifyDays(day_booked, month_booked, year_booked)
        
        if not verify_days.response["status"] == 'ok':
            return Response({
                "info": "Error al verificar los dias antes posibles al cancelar la reserva.",
                "sub_response": verify_days.response,
                "status": "no",
                "type": "VERIFY_DAYS_ERROR"
            }, 401)
        print(verify_days.response)
        #-> Verifica que si faltan 3 dias




        #-> Quita de la parte del usuario la reserva
        '''/crud/booking/remove.py'''
        print('------------')
        remove_booking = RemoveBooking(
            RemoveBooking.structure(
                day= day_booked,
                month= month_booked,
                year= year_booked,
                professional= responsable_appointment_booked,
                period= period_booked,
                start_time= start_time_booked,
                service_duration= services[service_booked][0],
                person_id= user_id,
                service_name= service_booked,
                id_appointment= id_reserva
            )
        )
        #-> Quita de la parte del usuario la reserva
        print('------------')

        #-> Verifica si pudo quitar la reserva del usuario sin problemas
        if not remove_booking.response["status"] == "ok":
            return Response(remove_booking.response, 401)
        #-> Verifica si pudo quitar la reserva del usuario sin problemas
        print('------------')
        print('llego a eliminar la resera correctamente')

        #-> Obtiene el resultado de forma éxitosa
        return Response({
            "info": "Se elimino la reserva correctamente",
            "status": "ok",
            "type": "SUCCESS",
            "data": remove_booking.response
        }, 200)
        #-> Obtiene el resultado de forma éxitosa

    except Exception as e:
        #print('bad2')
        return Response({
            "info": f"Error desconocdio del servidor: {e}",
            "status": "no",
            "type": "UNKNOW_ERROR"
        }, 500)


morning_time = Literal[
    '9:00',
    '9:30',
    '10:00',
    '10:30',
    '11:00',
    '11:30',
    '12:00',
    '12:30',
    '13:00',
    '13:30',  
        ]
afternoon_time = Literal[
            '15:00',
            '15:30',
            '16:00',
            '16:30',
            '17:00',
            '17:30',
            '18:00',
            '18:30',
            '19:00',
            '19:30',
        ]

class structureAdd(BaseModel):
    token_id: Optional[str] = None
    token_data: Optional[str] = None
    day_date: int
    month_date: int
    year_date: int
    hour: Union[
        morning_time,
        afternoon_time
    ]
    period: Literal['morning', 'afternoon']
    name_service: str

@router.post("/add")
async def Add_Appointment(request: Request, data: structureAdd):

    '''
    Ruta para **crear una reserva** del usuario
    
    Errores exitentes:
    - ERROR_DATABASE_DATE
    - UNKNOW_ERROR
    - SERVICE_ERROR
    '''

    try:
        day_date = data.day_date
        month_date = data.month_date
        year_date = data.year_date
        name_service = data.name_service
        hour = data.hour
        period = data.period
        user_id = request.state.user_id

        #@nb.jit(nopython=True)
        def Response(res: dict, status: int) -> JSONResponse:
            res["renew"] = {"token": request.state.new_token}
            return JSONResponse(res, status)
        

        day = datetime(year_date, month_date, day_date)
        
        try:
            
            #Verifica si existe existe la version del appointment_day y si esta vacia
            
            appointment = reservas.find_one({"fecha": {"$eq": day}})
            version_appointment = appointment["version"]

            if not appointment:
                return Response({
                "info": f"Hubo un error a al acceder esa ficha de reserva en ese día: {day}",
                "status": "no",
                "type": "ERROR_DATABASE_DATE"
            
                }, 401)    
        except Exception as e:
            return Response({
                "info": f"Hubo un error a al acceder esa ficha de reserva en ese día: {day}",
                "status": "no",
                "type": "ERROR_DATABASE_DATE"
            
            }, 401)
        print(version_appointment)
        
        #Arrays de varios tipos de profesion, y da el array de las personas que hay
        personal_raw = db_personal.find_one({ "version": version_appointment })
        print(personal_raw)

        '''
        Verificar que el usuario solo tenga de reservas 2, si lo supera
        '''

        personal = serviceToPersonal(
            serviceToPersonal.service(
                service= name_service
            )
        )
        #print(personal.response)

        if personal.response["status"] == 'no':
            return Response(personal.response, 401)

        #Obitene de la ficha general el personal especifico para saber el horario que tiene, y ver su estado
        specific_personal = personal_raw["personal"][personal.response["data"]]

        #Retorna una lista, donde los trabajadores con menos trabajo salen en los primeros de la lista
        worker_less_bussy = workerLessBusy(
            workerLessBusy.structure(
                rama_profesionales=specific_personal,
                professionals=appointment
            )
        )
        if not worker_less_bussy.response["status"] == 'ok':
            return Response(worker_less_bussy.response, 401)
        
        #print('worker less bussy->', worker_less_bussy.response["data"])

        #Obtiene todos los servicios procesadora para hacerse uso
        services = conversorServices()

        #print('services ->', services.response)

        if services is not None:
            if not services.response["status"] == 'ok':
                return Response(services.response, 401)
        else:
            return Response({
                "info": "Error al obtener los servicios.",
                "status": "no",
                "type": "SERVICE_ERROR"
            }, 401)

        services = services.response["data"]
        


        '''
        Luego de verificarse por JWT, en el middleware y puso bien su credenciales, pasa a hacer el booking
        aqui deberemos de acceder por por request.state, pluego validaremos o podriamos directamente validar
        con un parametro y especiifcar la estrtura con pydantic directamente

        Luego de sus datos y todas las funciones que estan operativas, comenzaria en hacerse el booking,
        claro aqui necesitariamos saber que servicio quiere, y que dia lo quiere hacer, luego con el usuario
        verificado pondiramos su propia credneciales y podriamos seguir.

        No tenemos que olvidar que aunque una respuesta este mal, debemos de devolverle otro token de renovación,
        y lo digo porque, cada vez que pasa por el middleware cambia la calve del usuario de jwt, y esto para verificar
        que lo hace bien todo el proceso
        '''
        
        booking = AddBooking(
            AddBooking.structure(
                day=day_date,
                month=month_date,
                year=year_date,
                professionals=worker_less_bussy.response["data"],
                period=period,
                start_time=hour,
                service_duration=services[name_service][0],
                person_id=user_id,
                service=name_service
            )
        )
        #print('aca', booking.response)
        
        if not booking.response["status"] == 'ok':
            return Response(booking.response, 401)
        
        return Response({
            "info": "La reserva se realizo de forma exitosa",
            "status": "ok",
            "type": "SUCCESS",
            "data": booking.response,
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