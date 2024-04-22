import sys

sys.path.append(r'C:\Users\slavu\PycharmProjects\ml_service')

from database.database import Base, SessionLocal, engine
from sqlalchemy import Column, Integer, String, ForeignKey, TIMESTAMP, Float, JSON
from models.user import User


class Transaction(Base):
    __tablename__ = "transaction"
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey(User.id))
    date = Column(TIMESTAMP)
    input_data = Column(JSON)
    output_data = Column(String)
    balance_change = Column(Float)
    status_code = Column(String)


# # Создание таблиц
if __name__ == "__main__":
    Base.metadata.create_all(engine)



