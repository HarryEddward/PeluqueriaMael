from fastapi import APIRouter

router = APIRouter(prefix="/restricted")


@router.get("/change_personal")
async def root():

    return 'change_personal'