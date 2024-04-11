from fastapi import APIRouter
from joblib import load
from models.schema import VineOutput, VineInput
from fastapi.responses import JSONResponse
import pandas as pd

try:
    model = load("./model")
except FileNotFoundError:
    model = None
    reason = "File 'model.pkl' not found. Model set to None."
except Exception as e1:
    model = None
    reason = "An error occurred while loading the model:" + str(e1)

model_router = APIRouter(tags=["Model"])
users = {}


@model_router.get("/healthcheck/")
def healthcheck():
    try:
        if model is not None:
            return JSONResponse(content={"message": "Service is ready"}, status_code=200)
        else:
            return JSONResponse(content={"message": f"Service is not ready. {reason}"}, status_code=500)
    except Exception as e2:
        return JSONResponse(content={"message": f"An error occurred: {e2})"}, status_code=500)


@model_router.post("/predict/")
def predict(data: VineInput):
    if model is None:
        return JSONResponse(content={"message": f"Service is not ready. {reason}"}, status_code=500)

    try:
        input_data = data.dict()
        input_df = pd.DataFrame(input_data, index=[0])
        quality = model.predict(input_df)[0]
        return VineOutput(predicted_quality=quality)
    except Exception as e3:
        return JSONResponse(content={"message": f"An error occurred: {e3})"}, status_code=500)
