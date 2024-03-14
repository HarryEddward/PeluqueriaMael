#Routing
from fastapi import (
    APIRouter,
    Request
)

#Database
#from ..database.db import SessionLocalStaff

#Models
from database.db import SessionLocalStaff

#Schemes
from database.models.staff import (
    Item
)
'''
db_item = Item(
        name=item.name,
        description=item.description
    )
db.add(db_item)
db.commit()
db.refresh(db_item)

return db_item
'''


# START ROUTES

router = APIRouter()

@router.get('/')
async def root():
    
    print(request.headers, request.body)

    return {
        "data": 0
    }

# END ROUTES