import sys

sys.path.append(r'C:\Users\slavu\Start_ML\4. MLService\ml_service')

from database.database import Base
from sqlalchemy import Column, Integer, String, Float
from services.ml.send_message import send_message
from models.user import BalanceBusiness
from models.transaction import TransactionBusiness
from datetime import datetime


class Model(Base):
    __tablename__ = "model"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    description = Column(String)
    price = Column(Float)


# # Создание таблиц
# if __name__ == "__main__":
#     Base.metadata.create_all(engine)


# # Добавление тестовой записи
# if __name__ == "__main__":
#     session = SessionLocal()
#     new_model = Model(name='model', description='Модель предсказывает оценку красного вина по его параметрам', price=100)
#     session.add(new_model)
#     session.commit()



