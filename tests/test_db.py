from datetime import datetime

from sqlalchemy import update

from models.user import User, Balance
from models.transaction import Transaction
from models.model import Model
from database.database import SessionLocal

import random
import string


def generate_random_string(length):
    letters = string.ascii_lowercase
    rand_string = ''.join(random.choice(letters) for i in range(length))
    return rand_string


def test_create_user():
    try:
        session = SessionLocal()
        user = User(login=generate_random_string(10), password=generate_random_string(10), first_name=generate_random_string(10),
                    last_name=generate_random_string(10), email=generate_random_string(10), admin=False)
        session.add(user)
        session.commit()
        assert True
    except:
        assert False


def test_create_admin():
    try:
        session = SessionLocal()
        new_user = User(login=generate_random_string(10), password=generate_random_string(10), first_name=generate_random_string(10),
                        last_name=generate_random_string(10), email=generate_random_string(10), admin=True)
        session.add(new_user)
        session.commit()
        assert True
    except:
        assert False

def test_create_model():
    try:
        session = SessionLocal()
        new_model = Model(name='model', description='Модель предсказывает оценку красного вина по его параметрам', price=100)
        session.add(new_model)
        session.commit()
        assert True
    except:
        assert False


def test_create_transaction():
    try:
        session = SessionLocal()
        transaction = Transaction(user_id=1,
                                  date=datetime.now(),
                                  input_data="{\"fixed_acidity\": 5, \"volatile_acidity\": 5, \"citric_acid\": 5, \"residual_sugar\": 5, \"chlorides\": 5, \"free_sulfur_dioxide\": 5, \"total_sulfur_dioxide\": 5, \"density\": 5, \"pH\": 5, \"sulphates\": 5, \"alcohol\": 5}",
                                  output_data="Предсказание модели: 5.679267365556076",
                                  balance_change=100, status_code="success")
        session.add(transaction)
        session.commit()
    except:
        assert False


def test_check_balance():
    try:
        session = SessionLocal()
        session.query(Balance).filter(Balance.user_id == 1).one()
    except:
        assert False


def test_top_up_balance():
    try:
        session = SessionLocal()
        balance = session.query(Balance).filter(Balance.user_id == 1).one()
        new_balance = balance.balance + 100
        balance_upd = update(Balance).where(Balance.user_id == 1).values(balance=new_balance)
        session.execute(balance_upd)
        session.commit()
    except:
        assert False


def test_write_off_balance():
    try:
        session = SessionLocal()
        balance = session.query(Balance).filter(Balance.user_id == 1).one()
        new_balance = balance.balance - 100
        balance_upd = update(Balance).where(Balance.user_id == 1).values(balance=new_balance)
        session.execute(balance_upd)
        session.commit()
    except:
        assert False




