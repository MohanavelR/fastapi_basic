from fastapi import FastAPI,HTTPException,Depends,status
from pydantic import BaseModel
import sqlite3
app=FastAPI()
# connect=sqlite3.connect("text.db",check_same_thread=False)
# cursor=connect.cursor()

# # cursor.execute('''
# #  create table if not exists users(
# #  id integer primary key autoincrement,
# #  name text not null,
# #  age integer

# #  )
# # ''')
# connect.commit()
# @app.get("/")
# def root():
#    return {"message":"Api start"}

# class UserBase(BaseModel):
#     name:str
#     age:int
# @app.post("/user")
# def create_user(user:UserBase):
#     try:
#      cursor.execute("insert into users(name,age) values(?,?)",(user.name,user.age))
#      return {"messge":"Successfully Added.."}  
#     except Exception as e:
#       raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,detail=str(e))        
    