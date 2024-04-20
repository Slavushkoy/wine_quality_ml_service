import pytest
from fastapi.testclient import TestClient
from api import app
from auth.authenticate import authenticate_cookie


@pytest.fixture(name="client")
def client_fixture():

    app.dependency_overrides[authenticate_cookie] = lambda: 9
    client = TestClient(app)
    yield client

    app.dependency_overrides.clear()

