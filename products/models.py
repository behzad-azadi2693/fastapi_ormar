import ormar
from config.settings import BaseMeta
from enum import Enum
from typing import Optional
from datetime import datetime
from sqlalchemy import func



class CategoryModel(ormar.Model):
    id:int = ormar.Integer(primary_key=True)
    name:str = ormar.String(max_length=255, unique=True)

    class Meta(BaseMeta):
        tablename = 'category'


class GENDER(Enum):
    man = 'MAN'
    women = 'WOMEN'
    child = 'CHILD'
    public = 'PUBLIC'


class ProductsModel(ormar.Model):
    id:int = ormar.BigInteger(primary_key=True)
    name:str = ormar.String(max_length=255)
    description:str = ormar.Text()
    attribute:str = ormar.JSON()
    gender = ormar.String(max_length=100, choices=list(GENDER))
    number:int = ormar.Integer()
    price:int = ormar.Integer()
    discount:float = ormar.Float(nullable=True, default=0.0)
    publish:bool = ormar.Boolean(default=False)
    created:datetime = ormar.DateTime(server_default=func.now(), nullable=True)
    category:Optional[CategoryModel] = ormar.ForeignKey(CategoryModel, related_name='all_product')

    class Meta(BaseMeta):
        tablename = 'products'


class ImageModel(ormar.Model):
    id:int = ormar.BigInteger(primary_key=True)
    image:str = ormar.String(max_length=1000)
    product:Optional[ProductsModel] = ormar.ForeignKey(ProductsModel, related_name='all_image')

    class Meta(BaseMeta):
        tablename = 'images'

class CommentsModel(ormar.Model):
    id:int = ormar.BigInteger(primary_key=True)
    name:str = ormar.String(max_length=255)
    messages:str = ormar.Text()
    product:Optional[ProductsModel] = ormar.ForeignKey(ProductsModel, related_name='all_comment')

    class Meta(BaseMeta):
        tablename = 'comments'