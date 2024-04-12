import sys

sys.path.append(r'C:\Users\slavu\Start_ML\4. MLService\ml_service')

from database.database import Base
from sqlalchemy import Column, Integer, String, Float
from ml_service.send_message import send_message
from models.user import BalanceBusiness
from models.transaction import TransactionBusiness
from datetime import datetime


class Model(Base):
    __tablename__ = "model"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    description = Column(String)
    price = Column(Float)


class ModelBusiness:
    @classmethod
    def predict(self, data, user_id, price=100):
        if BalanceBusiness.check_balance_binary(user_id):
            response = send_message(data)
            try:
                response = float(response)
                output_data = f'Предсказание модели: {response}'
                status = 'success'
                BalanceBusiness.write_off_balance(user_id=user_id, price=price)
                TransactionBusiness.add_transaction(user_id=user_id, date=datetime.now(), input_data=data,
                                                    output_data=output_data, balance_change=price,
                                                    status_code=status)
                response = {'status': status,
                            'response': response}
                return response
            except ValueError:
                status = 'error'
                TransactionBusiness.add_transaction(user_id=user_id, date=datetime.now(), input_data=data,
                                                    output_data=response, balance_change=0, status_code='error')
                response = {'status': status,
                            'response': response}
                return response
        else:
            status = 'fail'
            response = 'Недостаточно средств'
            TransactionBusiness.add_transaction(user_id=user_id, date=datetime.now(), input_data=data,
                                                output_data=response, balance_change=0, status_code='fail')
            response = {'status': status,
                        'response': response}
            return response


# # Создание таблиц
# if __name__ == "__main__":
#     Base.metadata.create_all(engine)

# # Добавление тестовой записи
# if __name__ == "__main__":
#     session = SessionLocal()
#     new_model = Model(name='model', description='Модель предсказывает оценку красного вина по его параметрам', price=100)
#     session.add(new_model)
#     session.commit()


# Проверка работы предсказаний
# if __name__ == "__main__":
#     import json
#
#     vine_input = {"fixed_acidity": 5,
#                   "volatile_acidity": 5,
#                   "citric_acid": 5,
#                   "residual_sugar": 5,
#                   "chlorides": 5,
#                   "free_sulfur_dioxide": 5,
#                   "total_sulfur_dioxide": 5,
#                   "density": 5,
#                   "pH": 5,
#                   "sulphates": 5,
#                   "alcohol": 5}
#     wine_json = json.dumps(vine_input)
#     result = ModelBusiness.predict(data=wine_json, user_id=1)
#     print(result)
