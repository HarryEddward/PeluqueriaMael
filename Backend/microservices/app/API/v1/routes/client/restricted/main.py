
from fastapi import (
    APIRouter,
    Request,
    HTTPException,
    status
)

router = APIRouter(prefix="/restricted")

@router.get('/hola')
async def root():
    
    return "hola"