import requests
import json

import pytest

from app.db import conn

BASE_URL = 'http://localhost:8000'
TEST_USER_ID = 'test'


@pytest.mark.parametrize('endpoint', [
    '/product/get',
    '/user/get',
    '/user/user001',
    '/product/product001',
    '/cart/user001',
    '/order/user001'
])
def test_endpoint_200(endpoint):
    resp = requests.get(f'{BASE_URL}{endpoint}')
    assert resp.status_code == 200


@pytest.mark.parametrize('endpoint', [
    '/product/not_exist_produtc',
    '/user/not_exist_user',
    '/cart/not_exist_user',
    '/order/not_exist_user',
])
def test_endpoint_404(endpoint):
    resp = requests.get(f'{BASE_URL}{endpoint}')
    assert resp.status_code == 404


@pytest.mark.parametrize('endpoint, payload', [
    ('/order/create', {'user_id': TEST_USER_ID}),
])
def test_create_order_with_empty_cart(endpoint, payload):
    _set_up_user()
    resp = requests.post(
        f'{BASE_URL}{endpoint}', data=json.dumps(payload)
    )
    assert resp.status_code == 400
    _tear_down_user()


def test_add_cart():
    _set_up_user()
    _tear_down_cart()
    for i in range(1, 4):
        payload = {
            'user_id': TEST_USER_ID,
            'product_id': 'product001',
            'quantity': i,
        }
        requests.post(f'{BASE_URL}/cart/add', data=json.dumps(payload))
    resp = requests.get(f'{BASE_URL}/cart/{TEST_USER_ID}')
    cart_d = resp.json()
    # quantity should sum up (1 + 2 + 3 = 6)
    assert cart_d['cart']['cart_items'] == [{'product_id': 'product001', 'quantity': 6}]
    _tear_down_cart()
    _tear_down_user()


def _set_up_user():
    cur = conn.cursor()
    cur.execute('''
        INSERT IGNORE INTO user (`user_id`, `name`)
        VALUES (%s, 'test user name')
    ''', (TEST_USER_ID,))
    cur.close()


def _tear_down_user():
    cur = conn.cursor()
    cur.execute('''
        DELETE FROM user
        WHERE user_id = %s
    ''', (TEST_USER_ID,))


def _tear_down_cart():
    cur = conn.cursor()
    cur.execute('''
        DELETE FROM cart
        WHERE user_id = %s
    ''', (TEST_USER_ID,))
