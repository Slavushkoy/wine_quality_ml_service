from fastapi.testclient import TestClient
import random
import string


def generate_random_string(length):
    letters = string.ascii_lowercase
    rand_string = ''.join(random.choice(letters) for i in range(length))
    return rand_string


username = generate_random_string(10)
password = generate_random_string(10)
first_name = generate_random_string(10)
last_name = generate_random_string(10)
email = generate_random_string(10)


def test_user_signup(client: TestClient):
    data_reg = {
        "login": username,
        "password": password,
        "first_name": first_name,
        "last_name": last_name,
        "email": email
    }
    response = client.post("/user/signup", json=data_reg)
    assert response.status_code == 200


def test_user_signin(client: TestClient):
    data = {
        'username': username,
        'password': password
    }
    response = client.post("/user/signin", data=data)
    assert response.status_code == 200


def test_home_token(client: TestClient):
    data = {
        'username': username,
        'password': password
    }
    response = client.post("/home/token", data=data)
    assert response.status_code == 200


def test_balance_check(client: TestClient):
    data = {
        'username': username,
        'password': password
    }
    response = client.post("/user/signin", data=data)
    token = response.json().get('access_token')

    headers = {"Authorization": f"Bearer {token}"}
    response = client.post("/balance/check", headers=headers)

    assert response.status_code == 200
    assert response.json()["message"] == "Ваш баланс составляет 300 кредитов"


def test_balance_check(client: TestClient):
    response = client.post("/balance/check")
    assert response.status_code == 200


def test_balance_top_up(client: TestClient):
    data = {
        "balance_add": 100
    }
    response = client.post("/balance/top_up", json=data)
    assert response.status_code == 200
    assert response.json()["message"] == "Операция выполнена успешно!"


def test_balance_top_up(client: TestClient):
    data = {
        "limit": 10
    }
    response = client.post("/transaction/show", data=data)
    assert response.status_code == 200


def test_transaction_show(client: TestClient):
    data = {
        "limit": 10
    }
    response = client.post("/transaction/show", data=data)
    assert response.status_code == 200


def test_model_predict(client: TestClient):
    payload = {
        'fixed_acidity': 0,
        'volatile_acidity': 0,
        'citric_acid': 0,
        'residual_sugar': 0,
        'chlorides': 0,
        'free_sulfur_dioxide': 0,
        'total_sulfur_dioxide': 0,
        'density': 0,
        'pH': 0,
        'sulphates': 0,
        'alcohol': 0
    }
    response = client.post(f"/model/predict/", json=payload)
    assert response.status_code == 200