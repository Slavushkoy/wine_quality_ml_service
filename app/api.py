from fastapi import FastAPI, HTTPException, Cookie
from starlette.responses import RedirectResponse
from routes.user import user_router
from routes.model import model_router
from routes.balance import balance_router
from routes.transaction import transaction_router
from routes.home import home_router

app = FastAPI(from_attributes=True)


@app.get("/")
async def home():
    return RedirectResponse(url="/docs")


# Register routes
app.include_router(user_router, prefix="/user")
app.include_router(model_router, prefix="/model")
app.include_router(balance_router, prefix="/balance")
app.include_router(transaction_router, prefix="/transaction")
app.include_router(home_router, prefix="/home")


@app.get("/protected_data")
def get_protected_data(auth_token: str = Cookie(None)):
    if auth_token != "your_auth_token":
        raise HTTPException(status_code=401, detail="Unauthorized")
    return {"data": "Protected data"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("api:app", host="0.0.0.0", port=8000, reload=True)

