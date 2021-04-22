import datetime
import sqlalchemy
from sqlalchemy import orm
from sqlalchemy_serializer import SerializerMixin
import os

from .db_session import SqlAlchemyBase


class Recipes(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'recipes'

    id = sqlalchemy.Column(sqlalchemy.Integer, 
                           primary_key=True, autoincrement=True)
    personal_id = sqlalchemy.Column(sqlalchemy.Integer, 
                                    sqlalchemy.ForeignKey("users.id"))
    name_recipe = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    cooking_time = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    start_date = sqlalchemy.Column(sqlalchemy.DateTime, 
                                     default=datetime.datetime.now)
    end_date = sqlalchemy.Column(sqlalchemy.DateTime, 
                                     default=datetime.datetime.now)
    ingredients = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    about = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    food = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    name_photo = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    category = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    coeff_popular = sqlalchemy.Column(sqlalchemy.Integer, default=0)
    user = orm.relation('User')