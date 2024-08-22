from pydantic import (
    BaseModel,
    ValidationError,
    constr
)
from abc import ABC, abstractmethod
from datetime import datetime

class Verify(ABC):

    class structure(BaseModel):
        pass
    


class AddBooking(Verify):
    
    class structure(BaseModel):
        user: constr(max_length=32)
        hour: datetime
        id_appointment: constr(max_length=50)

    def __init__(self) -> None:
        super().__init__()
