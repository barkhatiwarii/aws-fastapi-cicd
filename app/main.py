from fastapi import FastAPI, status
from mangum import Mangum
from pymongo import MongoClient
from pydantic import BaseModel
from typing import List
from bson.objectid import ObjectId
import urllib.parse
import json
from api.v1.api import router as api_router
password="root123"
username="barkha"
client = MongoClient(
    "mongodb+srv://"+urllib.parse.quote_plus(username)+":"+urllib.parse.quote_plus(password)+"@cluster0.otmoo.mongodb.net/myFirstDatabase?retryWrites=true&w=majority&ssl=true&ssl_cert_reqs=CERT_NONE"
)
db = client.get_database('myFirstDatabase')


app = FastAPI()

app.include_router(api_router, prefix="/api/v1")

DB = "myFirstDatabase"
COLLECTION = "users"

# Message class defined in Pydantic
class User(BaseModel):
    first_name: str
    last_name: str
    email: str
    mobile_number: int

@app.get("/",  tags=["Endpoint Test"])
def main_endpoint_test():
    return {"message": "Welcome CI/CD Pipeline with GitHub Actions!"}

def handler(event, context):
    event['requestContext'] = {}  # Adds a dummy field; mangum will process this fine  
    asgi_handler = Mangum(app)
    response = asgi_handler(event, context)
    return response

# adding user
@app.post("/user", status_code=status.HTTP_201_CREATED)
def post_user(user: User):
        collection = db["users"] 
        print(collection)
        result = collection.insert_one(user.dict())
        print(result)
        return {"message":"Data inserted successfully!!"}

# getting all users
@app.get("/user", response_model=List[User])
def get_users():
        collection = db["users"] 
        user_list = collection.find()
        users=[]
        for i in user_list:
            users.append(User(**i))
        print(users)
        return users

# updating user
@app.put("/user/{id}", status_code=status.HTTP_201_CREATED)
def update_user(id, user: User):
        collection = db["users"] 
        user_id=ObjectId(id)
        result = collection.update_one({"_id":user_id}, {"$set": dict(user)})
        print(result)
        return {"message":"User Data updated successfully!!"}

# deleting user
@app.delete("/user/{id}", status_code=status.HTTP_201_CREATED)
def delete_user(id):
        collection = db["users"] 
        user_id=ObjectId(id)
        result = collection.delete_one({"_id":user_id})
        print(result)
        return {"message":"User deleted successfully!!"}


# getting single user by id
@app.get("/user/{id}", response_model=List[User])
def get_users(id):
        collection = db["users"] 
        user_id=ObjectId(id)
        user = collection.find_one({"_id":user_id})
        print(user)
        return [user]
        
