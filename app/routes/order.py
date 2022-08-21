from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.models.order import (
    Order,
    BaseOrderException,
    CreateOrderPayload,
    CreateOrderResponse,
    GetOrdersResponse,
    OrderResponeModel,
)
from app.models.user import UserNotFoundException

router = APIRouter(
    prefix='/order',
    tags=['order']
)


class CreatOrderPayload(BaseModel):
    user_id: str


@router.post('/create', response_model=CreateOrderResponse)
def create_order(payload: CreateOrderPayload):
    try:
        order_id = Order.create_order(payload.user_id)
    except (
        UserNotFoundException, BaseOrderException
    ) as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)

    return {'order_id': order_id}


@router.get(
    '/{user_id}/{order_id}',
    response_model=OrderResponeModel,
    description='Get order by secific user'
)
def get_order(user_id: str, order_id: str):
    try:
        order = Order(user_id).query_order(order_id)
    except BaseOrderException as e:
        raise HTTPException(status_code=404, detail=e.detail)

    return {'order': order}


@router.get(
    '/{user_id}',
    response_model=GetOrdersResponse,
    description='Get all orders from a user'
)
def get_orders(user_id: str):
    try:
        orders = Order(user_id).query_orders()
    except (UserNotFoundException, BaseOrderException) as e:
        raise HTTPException(status_code=404, detail=e.detail)

    return {'orders': orders}
