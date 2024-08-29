from datetime import datetime, timedelta
from numpy import ushort
import numba as nb
from abc import ABC, abstractmethod


class Verify(ABC):

    @abstractmethod
    def __init__(self) -> None:
        super().__init__()
        pass

    @abstractmethod
    def verify(self) -> dict:
        pass

class verifyDays(Verify):

    #@nb.jit(nopython=True)
    def __init__(
            self,
            day: ushort,
            month: ushort,
            year: ushort
        ) -> None:
        self.day = day
        self.month = month
        self.year = year
        self.response = self.verify()

    #@nb.jit(nopython=True)
    def verify(self) -> dict:
        # Obtener la fecha actual
        current_date = datetime.now().date()

        # Crear objeto de fecha para la reserva
        reservation_date = datetime(self.year, self.month, self.day)
        reservation_date = reservation_date.date()

        #print('Tipo de current_date:', type(current_date))
        #print('Tipo de reservation_date:', type(reservation_date))


        # Calcular la diferencia entre las fechas
        difference = reservation_date - current_date
        #print('diference of the days: ', difference.days)

        # Si el número de dias es negativo es porque ya pasó la reserva, y si por algun motivo lo enseña al cliente pueda borrarlo. Pero seria problema del diseño de la API
        if difference.days < 0:
            return {
                "info": "La fecha de reserva es en el pasado. La reserva puede ser eliminado.",
                "status": "ok",
                "type": "SUCCESS"
            }

        # Verificar si faltan al menos 3 días para la reserva
        if not difference >= timedelta(days=3):
            
            return {
                "info": "No puede cancelar la reserva. Faltan menos de tres días.",
                "status": "no",
                "type": "LIMITED_EXCEEDED"
            }

            
        return {
            "info": "Tiene acceso a cancelar la reserva.",
            "status": "ok",
            "type": "SUCCESS"
        }
            