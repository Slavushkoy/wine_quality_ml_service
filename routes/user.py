from fastapi import APIRouter, HTTPException
from models.user import User
from models.schema import UserRegistration, UserAuthenticate

user_router = APIRouter(tags=["User"])
users = {}


@user_router.post("/registration")
def registration(data: UserRegistration):
    try:
        User.registration(login=data.login, password=data.password, first_name=data.first_name, last_name=data.last_name, email=data.email)
        return {"message": "User registered successfully"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@user_router.post("/authentication")
def registration(data: UserAuthenticate):
    try:
        answer = User.authenticate(login=data.login, password=data.password)
        if answer != False:
            return {"message": "User authenticated successfully"}
        else:
            return {"message": "Incorrect login or password"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

