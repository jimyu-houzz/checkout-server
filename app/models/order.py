import uuid
from datetime import datetime
from typing import List
from collections import defaultdict

import mysql.connector
from pydantic import BaseModel, Field

from app.db import conn
from app.db.base import connection_conf_d
from app.models.user import User, UserNotFoundException
from app.models.cart import Cart

GET_ORDER_COLUMNS = ('order_id', 'user_id', 'product_id', 'quantity', 'total', 'created')


class BaseOrderException(Exception):
    status_code = 400
    detail = 'Base order exception'


class CreatOrderError(BaseOrderException):
    detail = 'Create order failed'


class EmptyCartError(BaseOrderException):
    detail = 'Cart is empty'


class OrderNotFoundError(BaseOrderException):
    status_code = 404
    detail = 'Order not found'


class OrderAccessDeniedError(BaseOrderException):
    detail = 'Order access denied'


class CreateOrderPayload(BaseModel):
    user_id: str


class OrderItem(BaseModel):
    product_id: str
    quantity: int = Field(ge=0)


class OrderModel(BaseModel):
    order_id: str
    user_id: str
    total: float
    created: datetime
    items: List[OrderItem]


class CreateOrderResponse(BaseModel):
    order_id: str


class GetOrdersResponse(BaseModel):
    orders: List[OrderModel]


class OrderResponeModel(BaseModel):
    order: OrderModel


class Order:
    def __init__(self, user_id):
        user = User(user_id)
        if not user.exists:
            raise UserNotFoundException
        self.user_id = user_id

    def query_oids(self) -> List[str]:
        cur = conn.cursor()
        cur.execute('''
            SELECT order_id
            FROM `order`
            WHERE user_id = %s
        ''', (self.user_id,))
        oids = [row[0] for row in cur]
        cur.close()
        return oids

    def query_order(self, order_id: str) -> OrderModel:
        cur = conn.cursor()
        cur.execute('''
            SELECT o.order_id, user_id, product_id, quantity, total, o.created
            FROM `order` o
            JOIN order_item oi
                ON o.order_id = oi.order_id
            WHERE o.order_id = %s
        ''', (order_id,))
        order_ds = [dict(zip(GET_ORDER_COLUMNS, row)) for row in cur]
        cur.close()
        if not order_ds:
            raise OrderNotFoundError

        order_d = order_ds[0]
        if order_d['user_id'] != self.user_id:
            raise OrderAccessDeniedError

        created = order_d['created']
        total = order_d['total']
        items = [
            {
                'product_id': order_d['product_id'],
                'quantity': order_d['quantity'],
            } for order_d in order_ds
        ]

        return OrderModel(
            order_id=order_id,
            user_id=self.user_id,
            total=total,
            items=items,
            created=created
        )

    def query_orders(self) -> List[OrderModel]:
        oids = self.query_oids()
        result = []
        # TODO: fix n+1 query
        for oid in oids:
            result.append(self.query_order(oid))
        return result

    @staticmethod
    def create_order(user_id: str) -> str:
        try:
            cart = Order._query_cart_by_user_id(user_id)
        except Exception:
            raise

        total_price = 0
        cart_items = cart.cart_items
        product_ids = [cart_item.product_id for cart_item in cart_items]
        if not product_ids:
            raise EmptyCartError

        product_price_map = Order._query_product_price_map(product_ids)
        order_product_quantity_map = defaultdict(int)

        for cart_item in cart_items:
            total_price += product_price_map[cart_item.product_id] * cart_item.quantity
            order_product_quantity_map[cart_item.product_id] += cart_item.quantity

        # for simplicity, we simply take the first 16 elements
        order_id = str(uuid.uuid1())[:16]
        try:
            Order._insert_into_db(
                cart.user_id,
                order_id,
                total_price,
                order_product_quantity_map
            )
        except Exception as e:
            print(e)  # error loggin not implemented
            raise CreatOrderError

        return order_id

    @staticmethod
    def _query_cart_by_user_id(user_id: str):
        try:
            return Cart(user_id).get_cart()
        except UserNotFoundException:
            raise

    @staticmethod
    def _insert_into_db(
        user_id: str,
        order_id: str,
        total_price: float,
        order_product_quantity_map: dict
    ):

        ''' Example of order_product_quantity_map:
            {
                'product001': 3,
                'product002': 1,
            }
        '''
        # implement transaction with a new connection
        new_conn = mysql.connector.connect(**connection_conf_d)
        new_conn.start_transaction()
        cur = new_conn.cursor()
        try:
            cur.execute('''
                INSERT INTO `order` (`order_id`, `user_id`, `total`)
                VALUES (%s, %s, %s)
            ''', (order_id, user_id, total_price))

            cur.executemany('''
                INSERT INTO order_item (`order_id`, `product_id`, `quantity`)
                VALUES (%s, %s, %s)
            ''', [(order_id, product_id, quantity) for product_id, quantity in order_product_quantity_map.items()])

            cur.execute('''
                DELETE FROM cart
                WHERE user_id = %s
            ''', (user_id,))

            # NOTE: for simplicity, we do not reduce quantity in `product` table
            new_conn.commit()
        except Exception as e:
            print(e)
            new_conn.rollback()
            raise
        finally:
            cur.close()
            new_conn.close()

    @staticmethod
    def _query_product_price_map(product_ids: List[str]) -> dict:
        '''
            {
                'product001': 100,
                'product002': 200
            }
        '''

        if not product_ids:
            return {}

        # NOTE: mysql-conneter does not support list conversion
        # NOTE: str-formatting is prune to sql injection
        product_ids = [f'\'{id_}\'' for id_ in product_ids]
        product_id_str = "({})".format(','.join(product_ids))
        sql = '''
            SELECT product_id, price
            FROM product
            WHERE product_id in {}
        '''.format(product_id_str)
        cur = conn.cursor()
        cur.execute(sql)

        result = {row[0]: row[1] for row in cur}
        cur.close()
        return result
