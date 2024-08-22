from fastapi import APIRouter, HTTPException, Depends
from services.crud.user import BalanceBusiness
from models.schema import BalanceInput
from auth.authenticate import authenticate
from auth.authenticate import authenticate_cookie

balance_router = APIRouter(tags=["Balance"])
users = {}


@balance_router.post("/top_up")
async def registration(data: BalanceInput, user_id:str=Depends(authenticate_cookie)):
    try:
        if not user_id:
            user_id = Depends(authenticate)

        BalanceBusiness.top_up_balance(user_id=user_id, balance_add=data.balance_add)
        return {"message": "Операция выполнена успешно!"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@balance_router.post("/check")
async def registration(user_id:str=Depends(authenticate_cookie)):
    try:
        if not user_id:
            user_id = Depends(authenticate)

        balance = BalanceBusiness.check_balance(user_id=user_id)
        return {"message": f"Ваш баланс составляет {balance} кредитов"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@balance_router.post("/")
async def registration(user_id:str=Depends(authenticate)):
    try:
        if not user_id:
            user_id = Depends(authenticate)

        balance = BalanceBusiness.check_balance(user_id=user_id)
        return {"message": f"Ваш баланс составляет {balance} кредитов"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
