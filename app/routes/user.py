from fastapi import APIRouter, HTTPException, Depends, status
from services.crud.user import UserBusiness
from models.schema import UserRegistration, UserAuthenticate, TokenResponse
from fastapi.security import OAuth2PasswordRequestForm
from auth.jwt_handler import create_access_token
from auth.hash_password import HashPassword

user_router = APIRouter(tags=["User"])
hash_password = HashPassword()


@user_router.post("/signup")
async def registration(data: UserRegistration):
    try:
        hashed_password = hash_password.create_hash(data.password)
        UserBusiness.registration(login=data.login, password=hashed_password, first_name=data.first_name, last_name=data.last_name, email=data.email)
        return {"message": "Пользователь успешно зарегистрирован."}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@user_router.post("/signin", response_model=TokenResponse)
async def authentication(user: OAuth2PasswordRequestForm = Depends()) -> dict:
    user_exist = UserBusiness.get_user(user.username)
    if user_exist is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Пользователя с таким логином не существует")

    if hash_password.verify_hash(user.password, user_exist.password):
        access_token = create_access_token(user_exist.id)
        return {"access_token": access_token, "token_type": "Bearer"}

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Введен неккоретный пароль."
    )

