from fastapi import APIRouter, HTTPException
from models.user import BalanceBusiness
from models.schema import BalanceInput

balance_router = APIRouter(tags=["Balance"])
users = {}


@balance_router.post("/top_up")
def registration(data: BalanceInput):
    try:
        BalanceBusiness.top_up_balance(user_id=data.user_id, balance_add=data.balance_add)
        return {"message": "Операция выполнена успешно!"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@balance_router.post("/check")
def registration(user_id: int):
    try:
        balance = BalanceBusiness.check_balance(user_id=user_id)
        return {"message": f"Ваш баланс составляет {balance} кредитов"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))