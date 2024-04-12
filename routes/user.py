from fastapi import APIRouter, HTTPException
from models.user import UserBusiness
from models.schema import UserRegistration, UserAuthenticate

user_router = APIRouter(tags=["User"])
users = {}


@user_router.post("/registration")
def registration(data: UserRegistration):
    try:
        UserBusiness.registration(login=data.login, password=data.password, first_name=data.first_name, last_name=data.last_name, email=data.email)
        return {"message": "Пользователь успешно зарегистрирован."}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@user_router.post("/authentication")
def registration(data: UserAuthenticate):
    try:
        answer = UserBusiness.authenticate(login=data.login, password=data.password)
        if answer:
            return {"message": "Пользователь успешно аутентифицирован."}
        else:
            return {"message": "Логин или пароль введен не верно"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

