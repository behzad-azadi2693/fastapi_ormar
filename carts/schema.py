from pydantic import BaseModel
from fastapi import Body


class AddressSchema(BaseModel):
    name:str = Body(..., max_length=255)
    phone:str = Body(..., max_length=11, regex='^09\??\d{9,11}$')
    address:str = Body(...)
