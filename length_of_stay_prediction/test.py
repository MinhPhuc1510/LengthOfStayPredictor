# from sqlalchemy import create_engine, Column, Integer, String
# from sqlalchemy.orm import declarative_base, Session
from datetime import datetime
import pytz
# Base = declarative_base()

# class User(Base):
#     __tablename__ = "users"
#     id = Column(Integer, primary_key=True)
#     name = Column(String)

# engine = create_engine("sqlite:///:memory:")
# Base.metadata.create_all(engine)

# session = Session(engine)

# result = session.get(User, None)
# print(result)
  # Kết quả: None
now = datetime.now()
# print(now.astimezone('Europe/Amsterdam'))
datetime.now().astimezone("utc")
