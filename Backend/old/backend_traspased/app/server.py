from fastapi import (
    FastAPI,
    Depends
)
import uvicorn

from sqlalchemy.orm import Session





app = FastAPI()



#START ROUTING

from routes.user import router as router_public
from routes.staff import router as router_staff


app.include_router(router_public, prefix='/user')
app.include_router(router_staff, prefix='/staff')

#END ROUTING






# START MIDDLEWARE

'''
CORS
'''
from fastapi.middleware.cors import CORSMiddleware
from utils.security import allow

app.add_middleware(
    CORSMiddleware,
    allow_origins=allow["origins"],
    allow_credentials=True,
    allow_methods=allow["methods"],
    allow_headers=allow["headers"]
)


# END MIDDLEWARE






'''
class ItemCreate(BaseModel):
    name: str
    description: str



@app.post('/add')
def create_item(item: ItemCreate, db: Session = Depends(get_db_users)):

    db_item = Item(
        name=item.name,
        description=item.description
    )

    db.add(db_item)
    db.commit()
    db.refresh(db_item)

    return db_item
'''




if __name__ == "__main__":
    
    uvicorn.run(
        'server:app',
        host='127.0.0.1',
        port=9712,
        proxy_headers=True,
        #ssl_keyfile='ssl/peluqueriamael.com_key.txt',
        #ssl_certfile='ssl/peluqueriamael.com_cert/peluqueriamael.com.crt'
        reload=True
    )
