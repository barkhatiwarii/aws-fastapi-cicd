from fastapi import FastAPI
from mangum import Mangum
import json
from api.v1.api import router as api_router

app = FastAPI(title='Serverless Lambda FastAPI')

# app.include_router(api_router, prefix="/api/v1")


@app.get("/")
def main_endpoint_test():
    return {"message": "Welcome CI/CD Pipeline with GitHub Actions!"}


# to make it work with Amazon Lambda, we create a handler object
# handler = Mangum(app=app)
def handler(event, context):
    event['requestContext'] = {}  # Adds a dummy field; mangum will process this fine
    
    asgi_handler = Mangum(app)
    response = asgi_handler(event, context)
    json_data = event["queryStringParameters"] 
    # user = json_data["user"]
    return response

