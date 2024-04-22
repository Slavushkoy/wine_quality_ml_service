from fastapi import APIRouter, HTTPException, Depends
from services.crud.transaction import TransactionBusiness
from auth.authenticate import authenticate, authenticate_cookie

transaction_router = APIRouter(tags=["Transaction"])
users = {}


@transaction_router.post("/show")
async def registration(user_id: str = Depends(authenticate_cookie), limit: int = 10):
    try:
        if not user_id:
            user_id = Depends(authenticate)
        transactions = TransactionBusiness.show_transaction(user_id=user_id, limit=limit)
        return {"message": transactions}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

