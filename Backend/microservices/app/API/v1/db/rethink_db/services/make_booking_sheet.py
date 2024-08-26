from datetime import datetime, timedelta
from pymongo import DESCENDING
from uuid import uuid4
from abc import ABC, abstractmethod
from Backend.microservices.app.API.v1.db.mongodb.database import reservas, personal
from Backend.microservices.app.API.v1.db.rethink_db.database import reservas, connection


class Verify(ABC):
    
    @abstractmethod
    def __init__(self) -> None:
        super().__init__()

class BookingSheet(Verify):
    pass


if __name__ == "__main__":

    latest_personal: dict = personal.find_one(sort=[('_id', DESCENDING)])
    test_json: dict = {}
    test_json["professionals"] = {}
    json_professionals: dict = test_json["professionals"]

    for types_personal in latest_personal["personal"].keys():
        json_professionals[types_personal] = {}

    for profesional, staff in latest_personal["personal"].items():

        for person in staff:
            json_professionals[profesional][person] = {}

    test_json["version"] = latest_personal["version"]

    fecha_iso: datetime.isoformat = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0).isoformat()
    count_repeted_sheets = reservas.filter({"fecha": fecha_iso}).count().run(connection)

    if count_repeted_sheets == 0:

        test_json["fecha"] = fecha_iso
        reservas.insert(test_json).run(connection)
    else:
        pass

    print(BookingSheet)
