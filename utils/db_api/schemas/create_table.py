from sqlalchemy import String, Integer, Column, BigInteger
from sqlalchemy import sql
from utils.db_api.db_gino import db


class Items(db.Model):
    __tablename__ = 'products'
    id_product = Column(String)
    name = Column(String)
    description = Column(String)
    photo = Column(String)
    price = Column(Integer)

    query: sql.Select


class Users(db.Model):
    __tablename__ = 'users'
    id = Column(BigInteger, primary_key=True)
    name = Column(String)
    wallet = Column(Integer)
    referal_link = Column(String)

    query: sql.Select