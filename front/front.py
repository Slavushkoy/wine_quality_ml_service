from extra_streamlit_components import CookieManager
import streamlit as st
import requests

FASTAPI_URL = "http://api:8000"

# Создаем экземпляр CookieManager
cookie_manager = CookieManager()


def main():
    page = st.radio("Выбрать страницу", ["Регистрация и вход", "Предсказание", "Личный кабинет"])
    if page == "Регистрация и вход":
        if 'user_id' in cookie_manager.cookies:
            st.success("Пользователь авторизирован! Вы можете воспользоваться возможностями системы!")
        else:
            st.title('Авторизация')
            username = st.text_input('Ваш логин')
            password = st.text_input('Ваш пароль')
            data = {
                'username': username,
                'password': password
            }
            if st.button('Авторизация'):
                try:
                    response = requests.post(f"{FASTAPI_URL}/home/token", data=data)
                    if response.status_code == 200:
                        cookies = response.cookies.get_dict()
                        for key, value in cookies.items():
                            cookie_manager.set(key, value)
                    elif response.status_code == 404:
                        st.error(response.json()['detail'])
                    elif response.status_code == 401:
                        st.error(response.json()['detail'])
                    else:
                        st.error(response)
                except requests.exceptions.ConnectionError:
                    st.error("Service is not alive")
            st.title('Регистрация')
            username = st.text_input('Логин')
            password = st.text_input('Пароль')
            first_name = st.text_input('Имя')
            last_name = st.text_input('Фамилия')
            email = st.text_input('Email')

            data_reg = {
                "login": username,
                "password": password,
                "first_name": first_name,
                "last_name": last_name,
                "email": email
            }
            if st.button('Регистрация'):
                try:
                    response = requests.post(f"{FASTAPI_URL}/user/signup", json=data_reg)
                    if response.status_code == 200:
                        st.success(response.json()['message'])
                    elif response.status_code == 400:
                        st.error(response.json()['detail'])
                    else:
                        st.error(response)
                except requests.exceptions.ConnectionError:
                    st.error("Service is not alive")

    if page == "Предсказание":
        if 'user_id' in cookie_manager.cookies:
            st.title('Предсказание')

            # Input fields for all wine features
            fixed_acidity = st.number_input('Fixed Acidity', min_value=0.0, value=7.4, step=0.1)
            volatile_acidity = st.number_input('Volatile Acidity', min_value=0.0, value=0.7, step=0.01)
            citric_acid = st.number_input('Citric Acid', min_value=0.0, value=0.0, step=0.01)
            residual_sugar = st.number_input('Residual Sugar', min_value=0.0, value=1.9, step=0.1)
            chlorides = st.number_input('Chlorides', min_value=0.0, value=0.076, step=0.001)
            free_sulfur_dioxide = st.number_input('Free Sulfur Dioxide', min_value=0, value=11, step=1)
            total_sulfur_dioxide = st.number_input('Total Sulfur Dioxide', min_value=0, value=34, step=1)
            density = st.number_input('Density', min_value=0.0, value=0.9978, step=0.0001)
            pH = st.number_input('pH', min_value=0.0, value=3.51, step=0.01)
            sulphates = st.number_input('Sulphates', min_value=0.0, value=0.56, step=0.01)
            alcohol = st.number_input('Alcohol', min_value=0.0, value=9.4, step=0.1)

            # Button to make prediction
            if st.button('Предсказать'):
                # Form the request payload
                payload = {
                    'fixed_acidity': fixed_acidity,
                    'volatile_acidity': volatile_acidity,
                    'citric_acid': citric_acid,
                    'residual_sugar': residual_sugar,
                    'chlorides': chlorides,
                    'free_sulfur_dioxide': free_sulfur_dioxide,
                    'total_sulfur_dioxide': total_sulfur_dioxide,
                    'density': density,
                    'pH': pH,
                    'sulphates': sulphates,
                    'alcohol': alcohol
                }

                # Send the POST request to your FastAPI app
                try:
                    response = requests.post(f"{FASTAPI_URL}/model/predict/", json=payload,
                                             cookies=cookie_manager.cookies)
                    if response.status_code == 200:
                        st.success(response.json()['message'])
                    elif response.status_code == 400:
                        st.error(response.json()['message'])
                    else:
                        st.error(response)
                except requests.exceptions.ConnectionError:
                    st.error("Service is not alive")
        else:
            st.error("Пользователь не авторизирован! Войдите и попробуйте еще раз!")

    if page == "Личный кабинет":
        if 'user_id' in cookie_manager.cookies:
            st.title('Баланс')
            if st.button('Проверить баланс'):
                try:
                    response = requests.post(f"{FASTAPI_URL}/balance/check", cookies=cookie_manager.cookies)
                    if response.status_code == 200:
                        st.success(response.json()['message'])
                    elif response.status_code == 400:
                        st.error(response.json()['detail'])
                    else:
                        st.error(response)
                except requests.exceptions.ConnectionError:
                    st.error("Service is not alive")

            st.title('')
            balance_add = st.number_input('Введите сумму пополнения', min_value=0, value=100, step=100)

            data = {
                "balance_add": balance_add
            }
            if st.button('Пополнить баланс'):
                try:
                    response = requests.post(f"{FASTAPI_URL}/balance/top_up", json=data, cookies=cookie_manager.cookies)
                    if response.status_code == 200:
                        st.success(response.json()['message'])
                    elif response.status_code == 400:
                        st.error(response.json()['detail'])
                    else:
                        st.error(response)
                except requests.exceptions.ConnectionError:
                    st.error("Service is not alive")

            st.title('История предсказаний')
            limit = st.number_input('Введите количество записей для просмотра', min_value=0, value=10, step=1)
            data = {
                "limit": limit
            }
            if st.button('Показать историю предсказаний'):
                try:
                    response = requests.post(f"{FASTAPI_URL}/transaction/show", data=data, cookies=cookie_manager.cookies)
                    if response.status_code == 200:
                        transactions = response.json()['message']
                        for transaction in transactions:
                            fields = [f"{key}: {value}" for key, value in transaction.items()]
                            st.text('\n'.join(fields))
                    elif response.status_code == 400:
                        st.error(response.json()['detail'])
                    else:
                        st.error(response)

                except requests.exceptions.ConnectionError:
                    st.error("Service is not alive")
        else:
            st.error("Пользователь не авторизирован! Войдите и попробуйте еще раз!")


if __name__ == '__main__':
    main()
