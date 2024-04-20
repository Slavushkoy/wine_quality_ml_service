from sqlalchemy import Column, Integer, String, ForeignKey, Float, Boolean, BigInteger

import sys

sys.path.append(r'C:\Users\slavu\PycharmProjects\ml_service')

from database.database import Base, engine


class User(Base):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True, autoincrement=True)
    login = Column(String, unique=True)
    password = Column(String)
    first_name = Column(String)
    last_name = Column(String)
    email = Column(String, unique=True)
    admin = Column(Boolean, default=False)
    chat_id = Column(BigInteger, default=None)


class Balance(Base):
    __tablename__ = "balance"
    user_id = Column(Integer, ForeignKey(User.id), primary_key=True)
    balance = Column(Float)


# Создание таблиц
if __name__ == "__main__":
    Base.metadata.create_all(engine)

