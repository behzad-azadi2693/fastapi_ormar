import ormar
from accounts.models import UserModel
from config.settings import BaseMeta


class BasketModel(ormar.Model):
    id:int = ormar.Integer(primary_key=True)
    user:int = ormar.ForeignKey(UserModel)
    payed:bool = ormar.Boolean(default=False)

    class Meta(BaseMeta):
        tablename = 'Baskets'