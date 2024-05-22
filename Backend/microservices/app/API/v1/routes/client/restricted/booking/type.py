from to_literal.v1 import toLiteral
from db.database import types
from bson import ObjectId

def structureAdd_hour():

    """
    
    """
    
    try:
        config_hours = types.find_one({ "client.restricted.booking.types_add": { "$ne": {} } })
        morning_hours = config_hours["morning"]
        afternoon_hours = config_hours["afternoon"]

    except Exception as e:
        raise {
            "info": f"{e}",
            "status": "no",
            "type": "UNKNOW_ERROR"
        }