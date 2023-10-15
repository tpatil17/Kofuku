


from fastapi import FastAPI, Depends
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from pydantic import BaseModel
import requests
import random
from math import radians, sin, cos, sqrt, atan2

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

def distance(lat1, lon1, lat2, lon2): #distance between two users
    # Convert latitude and longitude from degrees to radians
    lat1, lon1, lat2, lon2 = map(radians, [float(lat1), float(lon1), float(lat2), float(lon2)])

    # Haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    r = 6371# radius of earht

    # Calculate the distance
    distance = r * c
    return distance

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
    

@app.post("/chosen_user")
async def startup(n: int, lim: int): # uses the input numbers to generate n users and find x closest users to plot
   
    random_users = get_random_users(n)
    k = random.randrange(n)
    r_fname = random_users[k]["name"]["first"]
    r_lname = random_users[k]["name"]["last"]
    r_lat  = random_users[k]["location"]["coordinates"]["latitude"]
    r_lon = random_users[k]["location"]["coordinates"]["longitude"]
    
    users_with_distances = []
    for i, u in enumerate(random_users):
        dist = distance(r_lat, r_lon, u["location"]["coordinates"]["latitude"], u["location"]["coordinates"]["longitude"])
        users_with_distances.append( (i,  dist) )

    nearest_users = sorted(users_with_distances, key=lambda x: x[1])[:lim]
   

    db = SessionLocal()
    for i, dist in nearest_users:
        user_profile = UserCreate(
            uid=i,
            email=random_users[i]["email"],
            first_name=random_users[i]["name"]["first"],
            last_name=random_users[i]["name"]["last"],
            gender=random_users[i]["gender"],
            latitude=random_users[i]["location"]["coordinates"]["latitude"],
            longitude=random_users[i]["location"]["coordinates"]["longitude"],
            run_id=random_users[i]["login"]["uuid"],
            dateTime=random_users[i]["registered"]["date"]
        )
        await create_item(user_profile, db)

    user_id_to_retrieve = k  # Replace with the user ID you want to retrieve
    user_data = db.query(Users).filter(Users.uid == user_id_to_retrieve).first()
    return [user_data, nearest_users, random_users]

 
    
