from fastapi import FastAPI



# This Create App
app=FastAPI(title="basic")

# Routers
@app.get("/") #BasePath
def index():
    return "Hello World"
@app.get("/return_json")
def return_json():
    return {"message":"Server is Running Successfully"}

