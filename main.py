from fastapi import FastAPI,Query,Path,Form,UploadFile,File,HTTPException,Cookie,Response,Request,Depends
from typing import Optional,List
# 
from pydantic import BaseModel,Field
import pandas as pd 
from PyPDF2 import PdfReader
import io
import uuid
# =============================
def global_level_dep(token:str="1234"):
   if token!="1234":
     raise HTTPException(status_code=401)
   else:
     return True   
# =============================   
# This Create App
app=FastAPI(title="basic",dependencies=[Depends(global_level_dep)])

# Routers
@app.get("/") #BasePath
def index():
    return "Hello World"

@app.get("/return_json")
def return_json():
    return {"message":"Server is Running Successfully"}

# Parameter
@app.get("/param/{id}")
def param(id:int):
    return {"data":f"Your Params is {id}"}
@app.get("/param/{name}/names")
def params(name):
     return {"data":f"Your Params is {name}"}

# Query Parameter
@app.get("/query")
def queryparam(limit,skip=0,sort:Optional[str]=None):
    return {"data":f"Your Query is Limit {limit} and Skip {skip} sort {sort}"}


# # Pydantic Model
# class Model(BaseModel): 
#     string:str
#     number:int
# class Blog(BaseModel):
#     title:str=Field(min_length=4,pattern="^[a-zA-Z]") #vaildation
#     # 
#     content:str
#     number:int=Field(gt=0,lt=10) #number Vaildation
#     is_publish:Optional[bool] =False
#     model:Model

# @app.post("/blog")
# def create_blog(req:Blog):
#     return {"message":f"Your Title:{req.title} and Your content:{req.content}"}    

#Quary
@app.get("/query_validation") # query Validation
def query_validation(id:int=Query(ge=10,lt=40,multiple_of=2)):
     return id

#Path
@app.get("/path_validation/{str}") # path Validation
def query_validation(str:str=Path(min_length=3,max_length=10)):
     return str

# Form 
@app.post("/form")
def form(name:str=Form(...),email:str=Form(...)):
    return{"name":name,"email":email}

# File Upload(single)
@app.post("/text_file_upload_single")
async def text_file_upload_single(file:UploadFile=File(...)):
    content= await file.read()
    try:
        text_pre=content
    except e :
        text_pre="Cannot Read Your Text file"    
    return {
    "content":text_pre,
    "filename":file.filename,
    "size":file.size,
    "type":file.content_type
}

# Text file Upload (Multiple)
@app.post("/text_file_upload_multiple")
async def text_file_upload_multiple(files:List[UploadFile]=File(...)):
    contents=[]
    for file in files:
      try:  
        content= await file.read()
        contents.append({
         "content":content,
         "filename":file.filename,
         "size":file.size,
         "type":file.content_type
        })
      except Exception as e :
        pass
    return {
        "contents":contents
    }

# file Upload(Excel)
@app.post("/file_upload_excel")
async def excel_file_upload_single(file:UploadFile=File(...)):
    content=await file.read()
    file_name=file.filename.lower()
    if file_name.endswith((".xls",".xlsx")):
       df=pd.read_excel(io.BytesIO(content))
       return {"Type":"Excel","preview":df.head(3).to_dict()}
    elif file_name.endswith(".pdf"):
        reader=PdfReader(io.BytesIO(content))
        text="".join([p.extract_text() or "" for p in reader.pages[:2]])
        return {"Type":"Pdf","preview":text.strip()[:300]}
    else:
        return {"Error":"Unsupported file format"}    

# Session
curr_username="mohan"
curr_password="mohan"
sessions={}
@app.post("/login_session")
def login_session(uname:str,pas:str,res:Response):
    if(curr_password==uname and curr_password==pas):
      sid=str(uuid.uuid4())
      sessions[sid]={"username":uname}
      res.set_cookie(key="sid",value=sid,httponly=True)
      return {'msg':"Login successfully "}
       
    else:
         raise HTTPException(status_code=401,detail="Invaild credentials")
@app.get("/home")
def home(sid:Optional[str]=Cookie(None)):
  if sid is None or sid not in sessions:
    raise HTTPException(status_code=401,detail="Not Authenticated")
  user=sessions[sid]
  return {"user":user}  


req_counter={}
max_req=5

@app.get("/rate_limit")
def get_data_rate_limit(req:Request):
  client_ip=req.client.host
  req_counter[client_ip]=req_counter.get(client_ip,0)+1
  print(req_counter)
  if req_counter[client_ip]> max_req:
     raise HTTPException(status_code=429,detail="reached your limit")
  return {"msg":"Successfully"}

# Dependency injection
# Funtion Level
def dep_db():
    return {"db":"Connected"}

@app.get("/dep")
async def dep(db:dict=Depends(dep_db)):
    return {"msg":"successfully","db_status":db}

# Class level

class Dep_class:
    def __init__(self):
     self.name="Mohan"
     self.age=22

def deb_class_value():
    return Dep_class()

@app.get("/dep_class")
def dep_class_level(user:Dep_class=Depends(deb_class_value)):
    return {"user":user}

#Global level
@app.get('/global_level')
def global_level():
    return {"message":"hello"} 

def gb_level():
    return {"message":"from gb"}
def parent(a=Depends(gb_level)):
    return {"message":f"from parents {a}"}
@app.get('/sub_dep')
def sub_dep_level(b:str=Depends(parent)):
    return {"message":b}

def sessionlocal():
    count = 1
    while True:
        count += 1
        yield count

counter = sessionlocal()

@app.get("/yield")
def yield_level():
    return {"count": next(counter)}