import sys

sys.path.append(r'C:\Users\slavu\Start_ML\4. MLService\ml_service')

from database.database import Base, SessionLocal, engine
from sqlalchemy import Column, Integer, ForeignKey, TIMESTAMP, JSON
from user import User


class Task(Base):
    __tablename__ = "task"
    user_id = Column(Integer, ForeignKey(User.id), primary_key=True)
    data_start = Column(TIMESTAMP)
    input_data = Column(JSON)


# Создание таблиц
# if __name__ == "__main__":
#     Base.metadata.create_all(engine)

