from fastapi import FastAPI
from routes.user import user_router
from routes.model import model_router
from routes.balance import balance_router
from routes.transaction import transaction_router


app = FastAPI(from_attributes=True)

# Register routes
app.include_router(user_router, prefix="/user")
app.include_router(model_router, prefix="/model")
app.include_router(balance_router, prefix="/balance")
app.include_router(transaction_router, prefix="/transaction")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("api:app", host="127.0.0.1", port=8000, reload=True)

