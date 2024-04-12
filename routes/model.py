from fastapi import APIRouter
from models.schema import VineInput
from models.model import ModelBusiness
from ml_service.send_message import send_message
import json
from fastapi.responses import JSONResponse


model_router = APIRouter(tags=["Model"])


@model_router.get("/healthcheck/")
def healthcheck():
    try:
        vine_input = {"fixed_acidity": 5,
                          "volatile_acidity": 5,
                          "citric_acid": 5,
                          "residual_sugar": 5,
                          "chlorides": 5,
                          "free_sulfur_dioxide": 5,
                          "total_sulfur_dioxide": 5,
                          "density": 5,
                          "pH": 5,
                          "sulphates": 5,
                          "alcohol": 5}
        wine_json = json.dumps(vine_input)
        result = send_message(wine_json)
        try:
            float(result)
            return JSONResponse(content={"message": "Service is ready"}, status_code=200)
        except ValueError:
            return JSONResponse(content={"message": f"Service is not ready."}, status_code=500)
    except Exception as e2:
        return JSONResponse(content={"message": f"An error occurred: {e2})"}, status_code=500)


@model_router.post("/predict/")
def predict(data: VineInput, user_id: int):
    vine_input_dict = data.dict()
    vine_input_json = json.dumps(vine_input_dict)
    response = ModelBusiness.predict(data=vine_input_json, user_id=user_id)
    if response['status'] == 'success':
        quality = response['response']
        quality = round(quality, 2)
        return JSONResponse(content={"message": f"Интересный выбор, оценка вашего вина: {quality} из 10"}, status_code=200)
    elif response['status'] == 'fail':
        return JSONResponse(content={"message": f"{response['response']}\nПополните баланс, и попробуйте еще раз."}, status_code=200)
    elif response['status'] == 'error':
        return JSONResponse(content={"message": f"{response['response']}\n'Возникла ошибка при валидации данных.\nПроверьте введенные значения и попробуйте еще раз'"},
                            status_code=200)
