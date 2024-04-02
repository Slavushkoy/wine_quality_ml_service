from sqlalchemy.exc import NoResultFound
from database.database import Base, SessionLocal, engine
from sqlalchemy import Column, Integer, String, ForeignKey, Float, Boolean
from sqlalchemy import update


class User(Base):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True, autoincrement=True)
    login = Column(String, unique=True)
    password = Column(String)
    first_name = Column(String)
    last_name = Column(String)
    email = Column(String, unique=True)
    admin = Column(Boolean, default=False)

    @classmethod
    def registration(cls, login, password, first_name, last_name, email):
        session = SessionLocal()
        new_user = User(login=login, password=password, first_name=first_name,
                        last_name=last_name, email=email, admin=False)
        # Проверка на уникальность логина и email
        if session.query(User).filter_by(login=login).first() or \
                session.query(User).filter_by(email=email).first():
            raise ValueError("Логин или email уже заняты")
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
                return True
            else:
                return False
        except NoResultFound:
            return False
        finally:
            session.close()


class Balance(Base):
    __tablename__ = "balance"
    user_id = Column(Integer, ForeignKey(User.id), primary_key=True)
    balance = Column(Float)

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
        if balance.balance > 100:
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


# Создание таблиц
# if __name__ == "__main__":
#     Base.metadata.create_all(engine)

# Регистрация тестового пользователя
# User.registration('login_dm', 'password_dm', 'first_name_dm', 'last_name_dm', 'email_dm')

# Обновление данных в таблице Balance
# Balance.check_balance(1)
# Balance.top_up_balance(1, 500)
# Balance.check_balance(1)
# Balance.check_balance_binary(1)
# Balance.write_off_balance(1, 100)
# Balance.check_balance(1)

# # Добавление тестового администратора
# if __name__ == "__main__":
#     session = SessionLocal()
#
#     new_user = User(login='admin_demo', password='demo_password', first_name='demo_first_name',
#                     last_name='demo_last_name', email='admin_demo_email', admin=True)
#     session.add(new_user)
#     session.commit()
