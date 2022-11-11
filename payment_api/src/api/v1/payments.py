from http import HTTPStatus

from fastapi import APIRouter

router = APIRouter()


@router.post("/", summary="Create a payment")
async def create_payment():
    return HTTPStatus.OK
