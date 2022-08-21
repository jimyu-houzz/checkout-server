from typing import Optional

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from app.models.Product import ProductNotFoundException
from app.models.User import UserNotFoundException
from app.models.Cart import Cart, CartModel

router = APIRouter(
    prefix='/cart',
    tags=['cart']
)


class AddProductPayload(BaseModel):
    user_id: str
    product_id: str
    quantity: int = Field(default=1, gt=0)


class RemoveProductPayload(BaseModel):
    user_id: str
    product_id: Optional[str] = Field(
        default_value=None,
        description='If product_id not provided, remove everything from cart'
    )


class GetCartResponseModel(BaseModel):
    cart: CartModel


@router.post(
    '/add',
    description='Without user session, we use route to specify user. This demo would allow anyone to add cart for each user.'
)
def add_product(payload: AddProductPayload):
    try:
        cart = Cart(payload.user_id)
        cart.add_product(payload.product_id, payload.quantity)
    except (UserNotFoundException, ProductNotFoundException) as e:
        raise HTTPException(status_code=404, detail=e.detail)

    return {}


@router.post(
    '/remove',
    description='''
    Removes product from cart.

    Without user session, we use route to specify user. This demo would allow anyone to remove cart for each user.
    NOTE: remove by specific product_id does not support spqcific quantity for now.
    '''
)
def remove_product(payload: RemoveProductPayload):
    try:
        cart = Cart(payload.user_id)
        if payload.product_id:
            cart.remove_product(payload.product_id)
        else:
            cart.remove_all()
    except (UserNotFoundException, ProductNotFoundException) as e:
        raise HTTPException(status_code=404, detail=e.detail)

    return {}


@router.get('/{user_id}', response_model=GetCartResponseModel)
def get_cart(user_id: str):
    try:
        cart_d = Cart(user_id).get_cart()
    except UserNotFoundException as e:
        raise HTTPException(status_code=404, detail=e.detail)

    return {'cart': cart_d}
