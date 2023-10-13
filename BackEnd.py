from fastapi import FastAPI,  Depends
from sqlalchemy import create_engine
from sqlalchemy.dialects.sqlite import *
from typing import List

from pydantic import BaseModel, constr
import requests

from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String


def get_random_users(n):
    random_users = []

    for _ in range(n):
        response = requests.get("https://randomuser.me/api/")
        if response.status_code == 200:
            data = response.json()
            user = data["results"][0]
            random_users.append(user)
        else:
            print("Failed to fetch a random user.")

    return random_users

n = 10  # Specify the number of random users you want
random_users = get_random_users(n)


Base = declarative_base()

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args = {"check_same_thread": False})

session = sessionmaker(autocommit=False, autoflush=False, bind=engine)

class Users(Base):
   __tablename__ = 'users'
   uid = Column(Integer, primary_key=True, nullable=False)
   email = Column(String(100))
   first_name = Column(String(50))
   last_name = Column(String(50))
   gender = Column(String(25))
   latitude = Column(String(100))
   longitude = Column(String(100))
   run_id = Column(String(100))
   dateTime = Column(String(100))
   Base.metadata.create_all(bind=engine)


class User(BaseModel):
    uid: int
    email: str
    first_name: str
    last_name: str
    gender: str
    latitude: str
    longitude: str
    run_id:str
    dateTime:str
    class Config:
        from_attributes = True

def get_db():
   db = session()
   try:
      yield db
   finally:
    db.close()



app = FastAPI()

@app.post("/users", response_model = User)
async def create_item(user: User,  db: Session = Depends(get_db)):
    usr =  User(uid= user.uid, email= user.email, first_name= user.first_name, last_name= user.last_name, gender= user.gender
               , latitude= user.latitude, longitude= user.longitude, run_id= user.run_id, dateTime= user.dateTime )
    db.add(usr)
    db.commit()
    db.refresh(usr)
    return usr


@app.get("/")
async def root():
    return {"message": "Hello World"}



for i in range(len(random_users)):
    user_profile = User(
        uid= i,
        email= random_users[i]["email"],
        first_name= random_users[i]["name"]["first"],
        last_name= random_users[i]["name"]["last"],
        gender= random_users[i]["gender"],
        latitude= random_users[i]["location"]["coordinates"]["latitude"],
        longitude= random_users[i]["location"]["coordinates"]["longitude"],
        run_id= random_users[i]["login"]["uuid"],
        dateTime= random_users[i]["registered"]["date"]
        )
    print(user_profile.first_name)
    create_item(user_profile)
