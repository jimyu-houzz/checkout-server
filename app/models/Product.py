from typing import List

from pydantic import BaseModel

from app.db import conn


PRODUCT_COLUMNS = ('product_id', 'title', 'price', 'quantiy')


class ProductModel(BaseModel):
    product_id: str
    title: str
    price: float
    quantiy: int


class ProductNotFoundException(Exception):
    statuc_code = 404
    detail = 'Produuct not found'


class Product:
    def __init__(self, product_id: str):
        self.product_id = product_id

    @property
    def exists(self):
        cur = conn.cursor()
        cur.execute('''
            SELECT COUNT(1)
            FROM product
            WHERE product_id = %s
            LIMIT 1
        ''', (self.product_id,))
        result = bool(cur.fetchone()[0])
        cur.close()
        return result

    @staticmethod
    def get_products(limit: int = 500) -> List[ProductModel]:
        cur = conn.cursor()
        cur.execute('''
            SELECT
                product_id,
                title,
                price,
                quantity
            FROM
                product
            LIMIT %s
        ''', (limit,))

        products = [ProductModel.parse_obj(dict(zip(PRODUCT_COLUMNS, row))) for row in cur]
        cur.close()

        return products

    def get(self) -> ProductModel:
        cur = conn.cursor()
        cur.execute('''
            SELECT
                product_id,
                title,
                price,
                quantity
            FROM
                product
            WHERE product_id = %s
        ''', (self.product_id,))
        row = cur.fetchone()
        if not row:
            raise ProductNotFoundException

        result = ProductModel.parse_obj(dict(zip(PRODUCT_COLUMNS, row)))
        cur.close()
        return result
