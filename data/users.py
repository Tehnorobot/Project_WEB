import datetime
import sqlalchemy
from sqlalchemy import orm
from .db_session import SqlAlchemyBase
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy_serializer import SerializerMixin
from flask_login import UserMixin

class User(SqlAlchemyBase, UserMixin, SerializerMixin):
    __tablename__ = 'users'
    id = sqlalchemy.Column(sqlalchemy.Integer, 
                           primary_key=True, autoincrement=True)
    surname = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    age = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    birth = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    email = sqlalchemy.Column(sqlalchemy.String, 
                              index=True, unique=True, nullable=True)
    hashed_password = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    modified_date  = sqlalchemy.Column(sqlalchemy.DateTime, 
                                     default=datetime.datetime.now)
    city_from = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    rec = orm.relation("Recipes", back_populates='user')
    
    def set_password(self, password):
        self.hashed_password = generate_password_hash(password)
        return self.hashed_password
    
    def check_password(self, password):
        return check_password_hash(self.hashed_password, password)