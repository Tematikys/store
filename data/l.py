import datetime
import sqlalchemy
from sqlalchemy import orm
from .db_session import SqlAlchemyBase

#создание корзины пользователя
class Likes(SqlAlchemyBase):
    __tablename__ = 'likes'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    item_name = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    user_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("users.id"))
    count = sqlalchemy.Column(sqlalchemy.Integer)
    user = orm.relation('User')
