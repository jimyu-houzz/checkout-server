from typing import List

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.models.Product import Product, ProductNotFoundException, ProductModel

router = APIRouter(
    prefix='/product',
    tags=['product']
)


class ProductResponseModel(BaseModel):
    product: ProductModel


class GetProductsReponseModel(BaseModel):
    products: List[ProductModel]


@router.get(
    '/get',
    response_model=GetProductsReponseModel,
    description='Get all products.'
)
def get_products():
    return {'products': Product.get_products()}


@router.get(
    '/{product_id}',
    response_model=ProductResponseModel,
    description='''
        Get a specific product.
        404 is returned if product does not exist.
    '''
)
def get(product_id: str):
    try:
        product = Product(product_id).get()
    except ProductNotFoundException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)
    return {'product': product}
