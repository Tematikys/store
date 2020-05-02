import datetime
import sqlalchemy
from .db_session import SqlAlchemyBase

# Создание таблицы Painters для хранения информации о художниках

class Category(SqlAlchemyBase):
    __tablename__ = 'Categories'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    Name = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    Picture = sqlalchemy.Column(sqlalchemy.String, nullable=True)
