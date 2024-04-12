import sys

sys.path.append(r'C:\Users\slavu\Start_ML\4. MLService\ml_service')

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


class TransactionBusiness:
    @classmethod
    def show_transaction(cls, user_id, limit: int = 10):
        session = SessionLocal()
        transactions = session.query(Transaction).filter(Transaction.user_id == user_id).order_by(Transaction.date.desc()).limit(limit).all()
        return transactions

    @classmethod
    def add_transaction(cls, user_id, date, input_data, output_data, balance_change, status_code):
        session = SessionLocal()
        new_user = Transaction(user_id=user_id, date=date, input_data=input_data, output_data=output_data, balance_change=balance_change, status_code=status_code)
        session.add(new_user)
        session.commit()


# # Создание таблиц
# if __name__ == "__main__":
#     Base.metadata.create_all(engine)


# # Тест
# # Получение списка транзакций для user_id=1
# transactions = TransactionBusiness.show_transaction(user_id=1)
#
# # Распечатка всех полей объектов класса Transaction
# for transaction in transactions:
#     for key, value in transaction.__dict__.items():
#         if key != '_sa_instance_state':
#             print(f"{key}: {value}")
