from fastapi import (
    APIRouter,
    Request,
    HTTPException,
    status,
    Response
)
from fastapi.responses import JSONResponse
from datetime import datetime
from bson import ObjectId
from typing import Optional
from typing import Literal
from typing import Union
import numba as nb
from pydantic import BaseModel
from pydantic import validator
from pydantic import ValidationError
from crud.mongodb.client.booking.utils.serviceToPersonal import serviceToPersonal
from crud.mongodb.client.booking.utils.workerLessBusy import workerLessBusy
from crud.mongodb.client.booking.utils.conversorServices import conversorServices
from crud.mongodb.client.booking.add import AddBooking as MDBAddBooking
from crud.mongodb.client.booking.remove import RemoveBooking as MDBRemoveBooking
from crud.rethink_db.booking.add import AddBooking as RDBAddooking
from crud.rethink_db.booking.remove import RemoveBooking as RDBRemoveBooking
from crud.mongodb.client.booking.utils.remove.verifyDays import verifyDays
from Backend.microservices.app.API.v1.routes.client.schemes.general import schemes
from Backend.microservices.app.API.v1.db.mongodb.database import reservas, configure, users, personal as db_personal
from Backend.microservices.app.API.v1.logging_config import logger
from Backend.microservices.app.API.v1.shared_microservices.cryptoapi.main import encrypt, decrypt
from Backend.microservices.app.API.v1.crud.mongodb.client.booking.validate.count_appointments import CountAppointmentsModel, CountAppointments 
from Backend.microservices.app.API.v1.db.redis_db.database import rate_limit, RedisClient

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


@router.options('/remove')
async def Remove_Appointment_From_Worker_Options(response: Response):

    response.headers["Allow"] = "POST, OPTIONS"
    response.headers["Content-Type"] = "application/json"
    return {
        "options": ["POST", "OPTIONS"]
    }


@router.post("/remove")
@rate_limit("3/10s")
async def Remove_Appointment_From_Worker(request: Request, data: structureRemove):

    """
    Ruta para **quitar las reservas** de los **clientes** como empleado.

    Chek if the employee exists and is verified from the CRUD, after
    from the email of the user entered and the ID of the appointment
    can delete without a restriction the user's appointment from
    MongoDB to RethinkDB.

    The ethic of the employee is important because even though the client
    want the perfect hour to book the appointment is important respect
    the time of the client, avoid to move between 1 hour more before or after.

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

        redis_clt = RedisClient.get_client()


        #-> Obtiene el usuario del id, y la ficha de reserva de ese día
        try:
            user_id: str = request.state.user_id
            id_reserva: str = data.id_reserva
            user = users.find_one(
                { "_id": ObjectId(user_id) },
                {f"data.reservas.{id_reserva}": 1, "_id": 0}
            )
            user = user['data']['reservas']

            #print(f'data.reservas.{id_reserva}:', user)
        except Exception as e:
            return Response({
                "info": "Error en la base de datos, quizas no exista y tengas mal los mismos parametros",
                "status": "no",
                "type": "DATABASE_ERROR"
            }, 401)
        
        if id_reserva not in user:
            #print('->', id_reserva)
            #print('->', id_reserva not in user)
            #print('->', user)

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

        #print(day_booked, month_booked, year_booked)
        #-> Parsea las variables para hacerlo úso en la ruta


        #-> Obtiene los servicios actuales para reservar
        services = conversorServices()
        logger.info("..............CONVERSOR SERVICES: %s", services)

        #print('services ->', services.response)

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
        #'''/crud/booking/utils/remove/verify_days.py'''

        """verify_days = verifyDays(day_booked, month_booked, year_booked)
        
        if not verify_days.response["status"] == 'ok':
            return Response({
                "info": "Error al verificar los dias antes posibles al cancelar la reserva.",
                "sub_response": verify_days.response,
                "status": "no",
                "type": "VERIFY_DAYS_ERROR"
            }, 401)"""
        #print(verify_days.response)
        #-> Verifica que si faltan 3 dias
        

        

        #-> Quita de la parte del usuario la reserva
        '''/crud/booking/remove.py'''
        #print('------------')
        remove_booking = MDBRemoveBooking(
            MDBRemoveBooking.structure(
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
        #print('------------')

        #-> Verifica si pudo quitar la reserva del usuario sin problemas
        if not remove_booking.response["status"] == "ok":
            return Response(remove_booking.response, 401)
        #-> Verifica si pudo quitar la reserva del usuario sin problemas
        #print('------------')
        #print('llego a eliminar la reserva correctamente')


        """logger.info("..........................................................")

        # Registrar el ID del usuario
        logger.info(f"user_id: {user_id}")

        # Registrar el ID de la reserva
        logger.info(f"id_reserva: {id_reserva}")

        # Registrar la reserva del usuario
        logger.info(f"user: {user}")

        # Registrar los detalles de la reserva
        logger.info(f"day_booked: {day_booked}")
        logger.info(f"month_booked: {month_booked}")
        logger.info(f"year_booked: {year_booked}")
        logger.info(f"period_booked: {period_booked}")
        logger.info(f"start_time_booked: {start_time_booked}")
        logger.info(f"responsable_appointment_booked: {responsable_appointment_booked}")
        logger.info(f"service_booked: {service_booked}")

        # Registrar los servicios obtenidos
        logger.info(f"services: {services}")

        # Registrar el resultado de la verificación de días
        logger.info(f"verify_days.response: {verify_days.response}")

        # Registrar el resultado de la eliminación de la reserva
        logger.info(f"remove_booking.response: {remove_booking.response}")

        # Registrar los datos de la reserva para RDB
        #logger.info(f"booking_data_rdb: {booking_data_rdb}")

        logger.info("..........................................................")"""

        type_personal: str

        if service_booked in services:
            type_personal = services[service_booked][2]
        
        booking_data_rdb: dict = {
            "date": datetime(year_booked, month_booked, day_booked),
            "personal_id": responsable_appointment_booked,
            "personal_type": type_personal,
            "appointment_id": id_reserva
        }
        booking_data_rdb_structure: RDBRemoveBooking.structure = RDBRemoveBooking.structure(**booking_data_rdb)
        result_booking_rdb = RDBRemoveBooking(booking_data_rdb_structure)

        if not result_booking_rdb.response["status"] == "ok":
            logger.error(f'{result_booking_rdb.response}')
            return Response(result_booking_rdb.response, 401)

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


@router.options('/add')
async def Add_Appointment_From_Worker_Options(response: Response):

    response.headers["Allow"] = "POST, OPTIONS"
    response.headers["Content-Type"] = "application/json"
    return {
        "options": ["POST", "OPTIONS"]
    }

@router.post("/add")
@rate_limit("5/10s")
async def Add_Appointment_From_Worker(request: Request, data: structureAdd):

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

        redis_clt = RedisClient.get_client()

        #@nb.jit(nopython=True)
        def Response(res: dict, status: int) -> JSONResponse:
            res["renew"] = {"token": request.state.new_token}
            return JSONResponse(res, status)
        

        day = datetime(year_date, month_date, day_date)

        data_count_appointments = CountAppointmentsModel(user_id=user_id)
        count_appointments = CountAppointments()
        result_count_appointments = count_appointments(data_count_appointments)

        if not result_count_appointments["status"] == "ok":
            return Response(result_count_appointments, 401)
        
        try:
            
            #Verifica si existe existe la version del appointment_day y si esta vacia
            
            appointment = reservas.find_one({"fecha": {"$eq": day}})
            logger.info('APPOINTMENT ADD: ', day)
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
        #print(version_appointment)
        
        #Arrays de varios tipos de profesion, y da el array de las personas que hay
        personal_raw = db_personal.find_one({ "version": version_appointment })
        #print(personal_raw)

        logger.info("APPOINTMENT: PASO 1")

        '''
        Verificar que el usuario solo tenga de reservas 2, si lo supera
        '''

        personal = serviceToPersonal(
            serviceToPersonal.service(
                service= name_service
            )
        )

        logger.info("APPOINTMENT: PASO 2")
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

        logger.info("APPOINTMENT: PASO 3")

        if not worker_less_bussy.response["status"] == 'ok':
            return Response(worker_less_bussy.response, 401)
        
        #print('worker less bussy->', worker_less_bussy.response["data"])

        #Obtiene todos los servicios procesadora para hacerse uso
        services = conversorServices()

        logger.info("APPOINTMENT: PASO 4")

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
        

        #######################################################
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
        
        booking = MDBAddBooking(
            MDBAddBooking.structure(
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

        logger.info("APPOINTMENT: PASO 5")
        #print('aca', booking.response)

        logger.info(f"APPOINTMENT: {booking.response}")
        
        if not booking.response["status"] == 'ok':
            return Response(booking.response, 401)
        #######################################################

        #######################################################
        hour_obj = datetime.strptime(hour, "%H:%M")
        hour_12 = hour_obj.strftime("%I:%M %p")

        user_raw: dict = users.find_one({ "_id": ObjectId(user_id) })
        user_email: str = user_raw["data"]["info"]["email"]
        decrypted_user_email: str = decrypt(user_email)
        
        logger.info("APPOINTMENT: PASO 7")

        logger.info(".............................")

        logger.info(f"Hour en str: {hour_12}")
        logger.info(f"Usuario del personal: {worker_less_bussy.response["data"][0][0]}")
        logger.info(f"Id reserva: {booking.response["data"]["id_appointment"]}")
        logger.info(f"Fecha: {day}")
        logger.info(f"Tipo de personal: {personal.response["data"]}")
        logger.info(f"Usuario: {user_email}")

        logger.info(".............................")

        booking_data_rdb: dict = {
            "user": decrypted_user_email,
            "date": day,
            "hour": hour_12,
            "id_appointment": booking.response["data"]["id_appointment"],
            "personal_type": personal.response["data"],
            "personal_id": worker_less_bussy.response["data"][0][0]
        }


        booking_rdb = RDBAddooking(
            RDBAddooking.structure(**booking_data_rdb)
        )

        logger.info("APPOINTMENT: PASO 8")

        if not booking_rdb.response["status"] == "ok":
            logger.info(f'error -> {booking_rdb.response}')
            return Response(booking_rdb.response, 401)

        logger.info("APPOINTMENT: Acabo 🧘")

        return Response(booking.response, 200)
        #######################################################
        

    except Exception as e:
        logger.error(f"ERROR APPOINTMENT: {e}")
        return JSONResponse({
            "info": f"Error desconocido por el servidor: {e}",
            "status": "no",
            "type": "UNKNOW_ERROR",
            "renew": {
                "token": request.state.new_token
            }
        }, 500)