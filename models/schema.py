from pydantic import BaseModel


class VineInput(BaseModel):
    fixed_acidity: float
    volatile_acidity: float
    citric_acid: float
    residual_sugar: float
    chlorides: float
    free_sulfur_dioxide: float
    total_sulfur_dioxide: float
    density: float
    pH: float
    sulphates: float
    alcohol: float

    class Config:
        from_attributes = True


class UserRegistration(BaseModel):
    login: str
    password: str
    first_name: str
    last_name: str
    email: str

    class Config:
        from_attributes = True


class UserAuthenticate(BaseModel):
    login: str
    password: str

    class Config:
        from_attributes = True


class BalanceInput(BaseModel):
    user_id: int
    balance_add: float

    class Config:
        from_attributes = True

