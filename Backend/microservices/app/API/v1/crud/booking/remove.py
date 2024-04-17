
from db.database import users
from pydantic import BaseModel


class RemoveBooking:

    def __init__(self) -> None:
        self.response = None

