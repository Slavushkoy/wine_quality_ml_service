from database.database import Base, SessionLocal, engine
from sqlalchemy import Column, Integer, String, Float


class Model(Base):
    __tablename__ = "model"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    description = Column(String)
    price = Column(Float)

    # # Предсказание
    # def predict(self, data):
    #     input_data = data.dict()
    #     input_df = pd.DataFrame(input_data, index=[0])
    #     quality = model.predict(input_df)[0]
    #     return VineOutput(predicted_quality=quality)


# Создание таблиц
# if __name__ == "__main__":
#     Base.metadata.create_all(engine)
#
# # Добавление тестового администратора
# if __name__ == "__main__":
#     session = SessionLocal()
#     new_model = Model(name='model', description='Модель предсказывает оценку красного вина по его параметрам', price=100)
#     session.add(new_model)
#     session.commit()