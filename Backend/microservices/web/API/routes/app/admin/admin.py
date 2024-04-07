from fastapi import APIRouter
import jwt


router = APIRouter()

@router.get("/items/{item_id}")
async def read_item(item_id: int):
    encoded_jwt = jwt.encode({
        "some": str(item_id)},
        "secret",
        algorithm="HS256"
     )

    return {"item_id": encoded_jwt}
