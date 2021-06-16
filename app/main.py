from fastapi import FastAPI, status
from mangum import Mangum
from pymongo import MongoClient
from pydantic import BaseModel
from typing import List
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
    json_data = event["queryStringParameters"] 
    # user = json_data["user"]
    return response

@app.post("/", status_code=status.HTTP_201_CREATED)
def post_message(user: User):
        msg_collection = db["users"] 
        # msg_collection = client[DB][COLLECTION]
        print(msg_collection)
        result = msg_collection.insert_one(user.dict())
        print(result)
        return {"message":"Data inserted successfully"}