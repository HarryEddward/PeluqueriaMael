from datetime import datetime, timedelta
from pymongo import DESCENDING
from uuid import uuid4
from pydantic import BaseModel
from numpy import ushort
from abc import ABC, abstractmethod
from typing import Dict
import json
from Backend.microservices.app.API.v1.db.mongodb.database import reservas, personal
from Backend.microservices.app.API.v1.db.rethink_db.database import reservas as RDBreservas, connection as RDBconnection
from Backend.microservices.app.API.v1.logging_config import logger





class ProfesionalsStructure:

    class generar_horarios(BaseModel):
        start_time_morning: str
        end_time_morning: str
        start_time_afternoon: str
        end_time_afternoon: str
    
    class generar_diccionario_profesionales(BaseModel):
        start_time_morning: str
        end_time_morning: str
        start_time_afternoon: str
        end_time_afternoon: str


class Verify_profesionals(ABC):
    
    @abstractmethod
    def generar_horarios(
        cls,
        data_raw: ProfesionalsStructure.generar_horarios
    ) -> dict:
        pass

    @abstractmethod
    def generar_diccionario_profesionales(
        cls,
        data_raw: ProfesionalsStructure.generar_diccionario_profesionales
        ) -> dict:
        pass


class Profesionals(Verify_profesionals):

    @classmethod
    def generar_horarios(cls, data_raw: ProfesionalsStructure.generar_horarios) -> dict:
        """
        Se require de 2 variables de las horas en formato 24 horas.
        Genera los horarios a partir de diferentes horarios
        de mañana y por la tarde, creando llaves en un diccionario
        de esos horarios entre 30' en cada horario.
        """
        try:
            # Desestructuración de datos validados
            data: dict = data_raw.model_dump()

            start_time_morning: str = data["start_time_morning"]
            end_time_morning: str = data["end_time_morning"]
            start_time_afternoon: str = data["start_time_afternoon"]
            end_time_afternoon: str = data["end_time_afternoon"]

            logger.info(f"{start_time_morning}")
            logger.info(f"{end_time_morning}")
            logger.info(f"{start_time_afternoon}")
            logger.info(f"{end_time_afternoon}")

            # Diccionario principal
            horarios = {}
            horarios["morning"] = {}
            horarios["afternoon"] = {}
            horario_morning = horarios["morning"]
            horario_afternoon = horarios["afternoon"]
            
            # Primer rango: Mañana
            inicio = datetime.strptime(start_time_morning, "%H:%M")
            fin = datetime.strptime(end_time_morning, "%H:%M")
            while inicio <= fin:
                hora_str = inicio.strftime("%H:%M")
                horario_morning[hora_str] = {}  # Diccionario vacío
                horario_morning[hora_str]["status"] = "libre"
                inicio += timedelta(minutes=30)
            
            # Segundo rango: Tarde
            inicio = datetime.strptime(start_time_afternoon, "%H:%M")
            fin = datetime.strptime(end_time_afternoon, "%H:%M")
            while inicio <= fin:
                hora_str = inicio.strftime("%H:%M")
                horario_afternoon[hora_str] = {}  # Diccionario vacío
                horario_afternoon[hora_str]["status"] = "libre"

                inicio += timedelta(minutes=30)
            #logger.info("->>>> %s", horarios)
            return horarios
        except Exception as e:
            logger.error(str(e))
            return {}

    
    @classmethod
    def generar_diccionario_profesionales(cls, data_raw: ProfesionalsStructure.generar_diccionario_profesionales) -> dict:
        """
        Genera un diccionario coherente de los profesionales
        disponibles listo para añadirse en la ficha de reservas
        """
        try:
            #Desestruturaión de datos validados
            data: dict = data_raw.model_dump()
            print(f"\n\ndata2: {data}")

            start_time_morning: str = data["start_time_morning"]
            end_time_morning: str = data["end_time_morning"]
            start_time_afternoon: str = data["start_time_afternoon"]
            end_time_afternoon: str = data["end_time_afternoon"]

            profesionals_proccessed: dict = {}
            profesionals_proccessed["professionals"] = {}
            profesionals_proccessed_professionals = profesionals_proccessed["professionals"]
            logger.info(profesionals_proccessed_professionals)

            hours: dict = cls.generar_horarios(
                data_raw=ProfesionalsStructure.generar_horarios(
                    start_time_morning=     start_time_morning,
                    end_time_morning=       end_time_morning,
                    start_time_afternoon=   start_time_afternoon,
                    end_time_afternoon=     end_time_afternoon
                )
            )

            last_version_personal_raw: dict = personal.find_one(sort=[('_id', DESCENDING)])

            last_version_personal: dict = last_version_personal_raw["personal"]
            
            for type_personal, list_personal in last_version_personal.items():
                
                for id_personal in list_personal:
                    profesionals_proccessed_professionals[id_personal] = hours

            profesionals_proccessed["version"] = last_version_personal_raw["version"]
            return profesionals_proccessed


        except Exception as e:
            logger.error(f"{e}")





class ORMongodbStructure:

    class verify_existent_sheet(BaseModel):
        fecha: datetime

    class generate_all_sheets(BaseModel):
        structure_profesionals_data: Dict
        number_of_sheets: int


class Verify_ORMongodb(ABC):
    
    @abstractmethod
    def verify_existent_sheet(
        cls,
        data_raw: ORMongodbStructure.verify_existent_sheet
    ) -> bool:
        pass

    @abstractmethod
    def generate_all_sheets(
        cls,
        data_raw: ORMongodbStructure.generate_all_sheets
    ) -> None:
        pass


class ORMongodb(Verify_ORMongodb):

    @classmethod
    def verify_existent_sheet(cls, data_raw: ORMongodbStructure.verify_existent_sheet) -> bool:
        """
        Verifica si la ficha de reserva de ese día se creó o no.
        """
        try:
            data: dict = data_raw.model_dump()
            fecha: datetime = data["fecha"]  # Asegúrate de que 'fecha' es un objeto datetime

            if not isinstance(fecha, datetime):
                raise ValueError("Fecha debe ser un objeto datetime")

            # Asegúrate de que la fecha es precisa hasta los segundos
            fecha = fecha.replace(microsecond=0)
            #logger.info(f"Fecha verificada: {fecha} (tipo: {type(fecha)})")

            # Verificar si el documento ya existe en la colección
            result_query: dict | None = reservas.find_one({"fecha": fecha})
            #logger.info(result_query)

            return result_query is not None

        except Exception as e:
            logger.error(str(e))
            return False

    @classmethod
    def generate_all_sheets(cls, data_raw: ORMongodbStructure.generate_all_sheets):
        """
        Genera fichas de reserva a partir de un numero determinado
        de fichas a partir del día que se crean, sumando los días adicionales.
        """
        try:
            data: dict = data_raw.model_dump()
            num_days_ahead: int = data["number_of_sheets"]
            structure_profesionals_data: dict = data["structure_profesionals_data"]

            start_date: datetime = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
            dates: list = [start_date + timedelta(days=i) for i in range(num_days_ahead)]

            for date in dates:
                result_sheet = cls.verify_existent_sheet(
                    ORMongodbStructure.verify_existent_sheet(fecha=date)
                )
                if not result_sheet:
                    structure_profesionals_data["fecha"] = date
                    # Elimina el campo "_id" si existe, para evitar duplicados
                    structure_profesionals_data.pop("_id", None)

                    reservas.insert_one(structure_profesionals_data)

                logger.info(f"Insertando documento para la fecha: {structure_profesionals_data}")
                #logger.info(f"Fecha ({date}): {result_sheet}")

        except Exception as e:
            logger.error(e)
            

if __name__ == "__main__":

    """
    Zona de testeo en desarrollo
    """
    structure_profesionals_data: dict = Profesionals.generar_diccionario_profesionales(
        data_raw=ProfesionalsStructure.generar_diccionario_profesionales(
            start_time_morning="09:00",
            end_time_morning="13:30",
            start_time_afternoon="15:00",
            end_time_afternoon="20:00"
        )
    )
    logger.info(f"{structure_profesionals_data}")

    
    ORMongodb.generate_all_sheets(
        data_raw=ORMongodbStructure.generate_all_sheets(
            structure_profesionals_data=structure_profesionals_data,
            number_of_sheets=120
        )
    )