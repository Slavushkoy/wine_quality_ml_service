from services.ml.send_message import send_message
from services.crud.user import BalanceBusiness
from services.crud.transaction import TransactionBusiness
from datetime import datetime


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
