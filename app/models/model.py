from sqlalchemy import Column, Integer, String, Float
import sys

sys.path.append(r'C:\Users\slavu\PycharmProjects\ml_service')

from database.database import Base, engine


class Model(Base):
    __tablename__ = "model"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    description = Column(String)
    price = Column(Float)


# Создание таблиц
if __name__ == "__main__":
    Base.metadata.create_all(engine)





