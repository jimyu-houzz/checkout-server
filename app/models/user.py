from typing import List

from pydantic import BaseModel

from app.db import conn

USER_COLUMNS = ('user_id', 'name')


class UserNotFoundException(Exception):
    status_code = 404
    detail = 'User not found'


class UserModel(BaseModel):
    user_id: str
    name: str


class User:
    def __init__(self, user_id: str):
        self.user_id = user_id

    @property
    def exists(self) -> bool:
        cur = conn.cursor()
        cur.execute('''
            SELECT COUNT(1)
            FROM user
            WHERE user_id = %s
            LIMIT 1
        ''', (self.user_id,))
        result = bool(cur.fetchone()[0])
        cur.close()

        return result

    @staticmethod
    def get_users(limit: int = 500) -> List[UserModel]:
        cur = conn.cursor()
        cur.execute('''
            SELECT user_id, name
            FROM user
            LIMIT %s
        ''', (limit,))

        result = [UserModel.parse_obj(dict(zip(USER_COLUMNS, row))) for row in cur]
        cur.close()
        return result

    def get(self) -> UserModel:
        cur = conn.cursor()
        cur.execute('''
            SELECT user_id, name
            FROM user
            WHERE user_id = %s
            LIMIT 1
        ''', (self.user_id,))
        row = cur.fetchone()
        if not row:
            raise UserNotFoundException
        return UserModel.parse_obj(dict(zip(USER_COLUMNS, row)))
