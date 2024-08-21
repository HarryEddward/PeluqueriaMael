
from Backend.microservices.app.API.v1.db.mongodb.database import users
from Backend.microservices.app.API.v1.logging_config import logger
from pydantic import BaseModel
from bson import ObjectId
import numba as nb
import pymongo.errors

class UserDelete:
    
    '''
    Se encarga de eliminar el usuario de forma compelta, pero claro 
    veríficara si tiene reservas pendientes y si tiene no podra borrar
    el usuario. Necesitara antes borrar de forma verificada cada reserva
    a aprtir de la ruta de /app/api/v1/client/restricted/booking/remove
    y la ruta que hará el delete se encargara antes de borrar en el
    usuario borrar y verificar que se puedan borrar las reservas. Quizás
    el usuario quiera borrar la cuenta por que no quiere asssistir en
    la reserva, pero no tenga la opción de poder eliminar la cuenta. Por
    tener una reserva pendiente.
    '''

    class structure(BaseModel):
        user_id: str
    
    #@nb.jit(nopython=True)
    def __init__(self, raw_data: structure) -> None:
        raw_data = raw_data.model_dump()
        user_id = raw_data["user_id"]

        self.response = self.remove(user_id)

    #@nb.jit(nopython=True)
    def remove(self, user_id):
        
        #Obtiene las reservas y luego verifica si no hay ningúna
        reservas = users.find_one({ "_id": ObjectId(user_id) }, { "_id": 0, "data.reservas": 1 })
        logger.info(reservas)
        logger.info(len(reservas) == 0)


        # Si no hay alguna reserva devolver que no debería tener
        if not reservas:
            print('Existen reservas.')
            return {
                "info": "Exiten reservas pendientes a verificar, no se puede eliminar la cuenta",
                "status": "no",
                "type": "APPOINTMENTS_EXISTENTS"
            }
        
        # Si no hay reservas pendientes a verificar, se eliminará la cuenta del usuario
        try:
            print('Como no existen reservas comienza a eliminar la cuenta.')
            users.delete_one({ "_id": ObjectId(user_id) })
        except Exception as e:
            return {
                "info": f"Error al eliminar la cuenta completa: {e}",
                "status": "no",
                "type": "DATABASE_ERROR"
            }
        
        print('Todo salió bien, se eliminó la cuenta exitosamente.')
        return {
            "info": "Se eliminó la cuenta de forma correcta",
            "status": "ok",
            "type": "SUCCESS"
        }