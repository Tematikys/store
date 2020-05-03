import datetime
import sqlalchemy
from .db_session import SqlAlchemyBase

#создание таблицы с товарами
class Item(SqlAlchemyBase):
    __tablename__ = 'Items'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    Title = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    Museum = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    Painter = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    Picture = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    Info = sqlalchemy.Column(sqlalchemy.String, nullable=True)
