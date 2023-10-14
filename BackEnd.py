


from fastapi import FastAPI, Depends
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from pydantic import BaseModel
import requests


# Database
DATABASE_URL = "sqlite:///./data.db"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

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

class UserCreate(BaseModel):
    uid: int
    email: str
    first_name: str
    last_name: str
    gender: str
    latitude: str
    longitude: str
    run_id: str
    dateTime: str

Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Random Users
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

app = FastAPI()

@app.post("/users", response_model=UserCreate)
async def create_item(user: UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(Users).filter(Users.uid == user.uid).first()
    if existing_user:
        existing_user.email = user.email
        existing_user.first_name = user.first_name
        db.commit()
        return {**user.model_dump(), "uid": existing_user.uid}
    else:
        user_instance = Users(**user.model_dump())
        db.add(user_instance)
        db.commit()
        return {**user.model_dump(), "uid": user_instance.uid}

@app.on_event("startup")
async def startup():
    n = 10  # Specify the number of random users you want
    random_users = get_random_users(n)
    db = SessionLocal()
    for i, user_data in enumerate(random_users):
        user_profile = UserCreate(
            uid=i,
            email=user_data["email"],
            first_name=user_data["name"]["first"],
            last_name=user_data["name"]["last"],
            gender=user_data["gender"],
            latitude=user_data["location"]["coordinates"]["latitude"],
            longitude=user_data["location"]["coordinates"]["longitude"],
            run_id=user_data["login"]["uuid"],
            dateTime=user_data["registered"]["date"]
        )
        await create_item(user_profile, db)
