import datetime
import sqlalchemy
from sqlalchemy import orm

from .db_session import SqlAlchemyBase

# Создание таблицы likes для хранения избранных картин пользователей

class Cart(SqlAlchemyBase):
    __tablename__ = 'Carts'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    picture = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    user_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("users.id"))
    user = orm.relation('User')