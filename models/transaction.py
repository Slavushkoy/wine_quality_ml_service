from database.database import Base, SessionLocal, engine
from sqlalchemy import Column, Integer, String, ForeignKey, TIMESTAMP, Float, JSON
from user import User


class Transaction(Base):
    __tablename__ = "transaction"
    user_id = Column(Integer, ForeignKey(User.id), primary_key=True)
    data_start = Column(TIMESTAMP)
    input_data = Column(JSON)
    data_end = Column(TIMESTAMP)
    output_data = Column(JSON)
    balance_change = Column(Float)
    status_code = Column(String)

    # Просмотр транзакций пользователя
    @classmethod
    def show_transaction(cls, user_id, limit: int = 10):
        session = SessionLocal()
        transactions = session.query(Transaction).filter(Transaction.user_id == user_id).order_by(Transaction.data_start.desc()).limit(limit).all()
        return transactions

# Создание таблиц
# if __name__ == "__main__":
#     Base.metadata.create_all(engine)



