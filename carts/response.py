from pydantic import BaseModel
from products.response import ProductResponse

class OrdersResponse(BaseModel):
    id:int
    product:list[ProductResponse]
    number:int

    class Config:
        orm_mode = True


class MyBasketResponse(BaseModel):
    id:int
    payed:bool
    moneyـpaid:float
    basket_orders:list[OrdersResponse]
    
    class Config:
        orm_mode = True


class BasketResponse(BaseModel):
    id:int
    user:int
    payed:bool
    moneyـpaid:float

    class Config:
        orm_mode = True