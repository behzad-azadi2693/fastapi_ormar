from pydantic import BaseModel
from fastapi import Body

class UserBase(BaseModel):
    phonenumber:str = Body(..., max_length=11, regex='^09\??\d{9,11}$')

class UserSchema(BaseModel):
    id:int
    phonenumber:int