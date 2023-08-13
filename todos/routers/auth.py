from fastapi import APIRouter


router = APIRouter()


@router.get("/auth")
async def auth_user():
    return {'user': "authenticated"}
