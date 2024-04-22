from sqlalchemy.exc import NoResultFound
from database.database import SessionLocal
from models.user import User, Balance
from sqlalchemy import update


class UserBusiness:
    @classmethod
    def registration(cls, login, password, first_name, last_name, email):
        session = SessionLocal()
        new_user = User(login=login, password=password, first_name=first_name,
                        last_name=last_name, email=email, admin=False)
        # Проверка на уникальность логина и email
        if session.query(User).filter_by(login=login).first() or \
                session.query(User).filter_by(email=email).first():
            raise ValueError("Login or email is already taken")
        session.add(new_user)
        session.commit()

        # Создание записи в таблице balance при создании записи в таблице user
        new_balance = Balance(user_id=new_user.id, balance=300)
        session.add(new_balance)
        session.commit()

    @classmethod
    def authenticate(cls, login, password):
        session = SessionLocal()
        try:
            user = session.query(User).filter(User.login == login).one()
            if user.password == password:
                return user.id
            else:
                return False
        except NoResultFound:
            return False
        finally:
            session.close()

    @classmethod
    def get_user(cls, login):
        session = SessionLocal()
        try:
            user = session.query(User).filter(User.login == login).one()
            return user
        except NoResultFound:
            return None
        finally:
            session.close()

    @classmethod
    def add_chat_id(cls, user_id, chat_id):
        session = SessionLocal()
        try:
            # Проверяем, существует ли уже пользователь с таким chat_id
            existing_user = session.query(User).filter(User.chat_id == chat_id).first()
            if existing_user:
                # Очищаем chat_id в старых записях
                session.query(User).filter(User.chat_id == chat_id).update({"chat_id": None})

            # Обновляем информацию о пользователе
            session.query(User).filter(User.id == user_id).update({"chat_id": chat_id})
            session.commit()
        except Exception as e:
            session.rollback()
            return e
        finally:
            session.close()

    @classmethod
    def get_user_id(cls, chat_id):
        session = SessionLocal()
        try:
            user = session.query(User).filter(User.chat_id == chat_id).one()
            return user.id
        except Exception as e:
            session.rollback()
            return e
        finally:
            session.close()


class BalanceBusiness:
    # Проверка баланса пользователем
    @classmethod
    def check_balance(cls, user_id):
        session = SessionLocal()
        balance = session.query(Balance).filter(Balance.user_id == user_id).one()
        return balance.balance

    # Проверка баланса на достаточность средств для предсказания
    @classmethod
    def check_balance_binary(cls, user_id):
        session = SessionLocal()
        balance = session.query(Balance).filter(Balance.user_id == user_id).one()
        if balance.balance >= 100:
            return True
        else:
            return False

    # Пополнение баланса
    @classmethod
    def top_up_balance(cls, user_id, balance_add):
        session = SessionLocal()
        balance = session.query(Balance).filter(Balance.user_id == user_id).one()
        new_balance = balance.balance + balance_add
        balance_upd = update(Balance).where(Balance.user_id == user_id).values(balance=new_balance)
        session.execute(balance_upd)
        session.commit()

    # Списание средств за предсказание
    @classmethod
    def write_off_balance(cls, user_id, price):
        session = SessionLocal()
        balance = session.query(Balance).filter(Balance.user_id == user_id).one()
        new_balance = balance.balance - price
        balance_upd = update(Balance).where(Balance.user_id == user_id).values(balance=new_balance)
        session.execute(balance_upd)
        session.commit()
