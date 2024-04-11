from fastapi import APIRouter, HTTPException
from models.transaction import Transaction

transaction_router = APIRouter(tags=["Transaction"])
users = {}


@transaction_router.post("/show")
def registration(user_id: int, limit: int = 10):
    try:
        Transaction.show_transaction(user_id=user_id, limit=limit)
        return Transaction.show_transaction(user_id=user_id, limit=limit)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

