
from serviceToPersonal import serviceToPersonal

class knowAppointments:

    '''
    Verifica si tiene otras reservas del usuario para así no poder hacer mas reservas que la misma
    persona tiene

    Saber la version del personal de la ficha
    Obtener el personal de la version especificada
    '''

    def __init__(self) -> None:
        self.response = self.know_appointments()

    def know_appointments(self) -> None:
        
        serviceToPersonal(
            serviceToPersonal.service()
        )