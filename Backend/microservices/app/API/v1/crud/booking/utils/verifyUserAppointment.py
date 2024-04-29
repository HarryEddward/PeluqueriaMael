

class verifyUserAppointment:

    '''
    Verifica si tiene otras reservas del usuario para así no poder hacer mas reservas que la misma
    persona tiene
    '''

    def __init__(self) -> None:
        self.response = self.know_appointments()

    def know_appointments(self) -> None:
        pass