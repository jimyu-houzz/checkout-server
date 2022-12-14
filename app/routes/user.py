from typing import List

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.models.user import User, UserNotFoundException, UserModel

router = APIRouter(
    prefix='/user',
    tags=['user']
)


class UserResponseModel(BaseModel):
    user: UserModel


class GetUsersReponseModel(BaseModel):
    users: List[UserModel]


@router.get(
    '/get',
    response_model=GetUsersReponseModel,
    description='Get all users.'
)
def get_users():
    users = User.get_users()
    return {'users': users}


@router.get(
    '/{user_id}',
    response_model=UserResponseModel,
    description='For simplicity, add/remove user functionalities are not implemented.'
)
def get_user(user_id: str):
    try:
        user = User(user_id).get()
    except UserNotFoundException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)
    return {'user': user}
