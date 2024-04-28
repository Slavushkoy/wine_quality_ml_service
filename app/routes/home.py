from fastapi import APIRouter, Depends, HTTPException, status, Response
from fastapi.security import OAuth2PasswordRequestForm
from decouple import config
from auth.jwt_handler import create_access_token
from auth.hash_password import HashPassword
from services.crud.user import UserBusiness

hash_password = HashPassword()
home_router = APIRouter(tags=["Home"])


@home_router.post("/token")
async def login_for_access_token(response: Response, form_data: OAuth2PasswordRequestForm=Depends()) -> dict[str, str]:
    user_exist = UserBusiness.get_user(login=form_data.username)
    if user_exist is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Пользователя с таким логином не существует")

    if hash_password.verify_hash(form_data.password, user_exist.password):
        access_token = create_access_token(user_exist.id)
        response.set_cookie(
            key=config('COOKIE_NAME'),
            value=f"Bearer {access_token}",
            httponly=True

        )

        return {config('COOKIE_NAME'): access_token, "token_type": "bearer"}

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Введен неккоретный пароль."
    )


@home_router.get("/logout")
async def delete_cookie(response: Response):
    response.delete_cookie("cookie_name")
    return {"message": "Cookie удалена"}






