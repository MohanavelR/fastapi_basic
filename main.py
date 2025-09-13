from fastapi import FastAPI



# This Create App
app=FastAPI()

# Routers
@app.get("/")
def index():
    return "Hello World"
@app.get("/return_json")
def return_json():
    return {"message":"Server is Running Successfully"}

