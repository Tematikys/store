import datetime
import sqlalchemy
from .db_session import SqlAlchemyBase

#создание таблицы с товарами
class Item(SqlAlchemyBase):
    __tablename__ = 'Items'

    name = sqlalchemy.Column(sqlalchemy.String, primary_key=True)
    category = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    picture = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    info = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    price = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    count = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
