import ormar
from accounts.models import UserModel
from products.models import ProductsModel
from config.settings import BaseMeta
from typing import Optional


class BasketModel(ormar.Model):
    id:int = ormar.Integer(primary_key=True)
    user:Optional[UserModel] = ormar.ForeignKey(UserModel, related_name='user_baskets')
    payed:bool = ormar.Boolean(default=False)
    moneyـpaid:float = ormar.Float(default=0.0, nullable=True)

    class Meta(BaseMeta):
        tablename = 'basket'


class OrdersModel(ormar.Model):
    id:int = ormar.BigInteger(primary_key=True)
    basket:Optional[BasketModel] = ormar.ForeignKey(BasketModel, related_name = 'basket_orders')
    product:Optional[ProductsModel] = ormar.ForeignKey(ProductsModel, related_name = 'product_orders')
    number:int = ormar.Integer(default=1, nullable=True)

    class Meta(BaseMeta):
        tablename = 'orders'


class AddressModel(ormar.Model):
    id:int = ormar.Integer(primary_key=True)
    name:str = ormar.String(max_length=255)
    phone:str = ormar.String(max_length=15)
    address:str = ormar.Text()
    basket:Optional[BasketModel] = ormar.ForeignKey(BasketModel, related_name='basket_address')

    class Meta(BaseMeta):
        tablename = 'address'
    