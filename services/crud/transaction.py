from database.database import SessionLocal
from models.transaction import Transaction


class TransactionBusiness:
    @classmethod
    def show_transaction(cls, user_id, limit: int = 10):
        session = SessionLocal()
        transactions = session.query(Transaction).filter(Transaction.user_id == user_id).order_by(
            Transaction.date.desc()).limit(limit).all()
        return transactions

    @classmethod
    def add_transaction(cls, user_id, date, input_data, output_data, balance_change, status_code):
        session = SessionLocal()
        new_user = Transaction(user_id=user_id, date=date, input_data=input_data, output_data=output_data,
                               balance_change=balance_change, status_code=status_code)
        session.add(new_user)
        session.commit()

