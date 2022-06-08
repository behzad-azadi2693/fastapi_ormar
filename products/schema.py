from fastapi import File, UploadFile, Body
from pydantic import BaseModel, validator
from enum import Enum
from typing import Optional, Dict, Any


class GENDER(str, Enum):
    man = 'MAN'
    women = 'WOMEN'
    child = 'CHILD'
    public = 'PUBLIC'

class ProductSchema(BaseModel):
    name:str = Body(..., max_length=255)
    description:str = Body(...)
    attribute: str
    gender: GENDER
    number:int = Body(..., ge=1)
    price:int = Body(..., ge=0)
    discount:float = Body(None)
    publish:Optional[bool] = False
    image:list[UploadFile]=File(...)


    @validator('image')
    def check_image(cls, v, **kwargs):
        for img in v:
            if not img.content_type in ['image/png', 'image/jpg', 'image/jpeg']:
                return HTTPException(status_code=400, detail='filds must be image')
        return v

