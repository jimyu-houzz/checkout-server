from typing import List, Optional

from pydantic import BaseModel

from app.models.User import User, UserNotFoundException
from app.models.Product import Product, ProductNotFoundException
from app.db import conn

CART_COLUMNS = ('product_id', 'quantity')


class CartItem(BaseModel):
    product_id: str
    quantity: int


class CartModel(BaseModel):
    user_id: str
    cart_items: List[CartItem]


class Cart:
    def __init__(self, user_id: str):
        user = User(user_id)
        if not user.exists:
            raise UserNotFoundException
        self.user_id = user_id

    def get_cart(self) -> CartModel:
        cur = conn.cursor()
        cur.execute('''
            SELECT product_id, SUM(quantity)
            FROM cart
            WHERE user_id = %s
            GROUP BY product_id
        ''', (self.user_id,))
        cart_items = [CartItem.parse_obj(dict(zip(CART_COLUMNS, row))) for row in cur]
        cur.close()

        return CartModel(user_id=self.user_id, cart_items=cart_items)

    def add_product(self, product_id: str, quantity: int):
        product = Product(product_id)
        if not product.exists:
            raise ProductNotFoundException
        cur = conn.cursor()
        cur.execute('''
            INSERT INTO cart (`user_id`, `product_id`, `quantity`)
            VALUES (%s, %s, %s)
        ''', (self.user_id, product_id, quantity))
        cur.close()

    def remove_product(self, product_id: str):
        cur = conn.cursor()
        cur.execute('''
            DELETE FROM cart
            WHERE user_id = %s
            AND product_id = %s
        ''', (self.user_id, product_id))
        cur.close()

    def remove_all(self):
        cur = conn.cursor()
        cur.execute('''
            DELETE FROM cart
            WHERE user_id = %s
        ''', (self.user_id,))
        cur.close()