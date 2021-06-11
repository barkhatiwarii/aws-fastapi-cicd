from mangum import Mangum
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Hello World"}

handler = Mangum(app=app)
