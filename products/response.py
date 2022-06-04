from pydantic import BaseModel


class ImageResponse(BaseModel):
    image:str

    class Config:
        orm_mode = True


class CategoryProductResponse(BaseModel):
    id:int
    name:str 
    price:int
    discount:float

    class Config:
        orm_mode = True


class CategoryResponse(BaseModel):
    name:str
    all_product:list[CategoryProductResponse] | None

    class Config:
        orm_mode = True


class CommentResponse(BaseModel):
    name:str 
    messages:str 

    class Config:
        orm_mode = True


class ProductResponse(BaseModel):
    name:str
    description:str
    attribute:dict
    sex:str
    number:int
    price:int
    discount:float 
    publish:bool
    all_image:list[ImageResponse] | None
    all_comment:list[CommentResponse] | None

    class Config:
        orm_mode = True