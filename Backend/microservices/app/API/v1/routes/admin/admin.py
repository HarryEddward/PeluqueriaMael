from fastapi import APIRouter
import jwt
from routes.admin.restricted.main import router as restricted_router

router = APIRouter()
router.include_router(restricted_router)

@router.get("/")
async def read_item(item_id: int):
    
    """
    Obtiene la información del usuario actualmente autenticado.

    Args:
        token (str, opcional): El token de autenticación.

    Returns:
        dict: La información del usuario autenticado.
    """
    
    encoded_jwt = jwt.encode({
        "some": str(item_id)},
        "secret",
        algorithm="HS256"
     )

    return {"item_id": encoded_jwt}
