import ormar
from config.settings import BaseMeta


class UserModel(ormar.Model):
    id:int = ormar.BigInteger(primary_key=True)
    phonenumber:int = ormar.Integer(min_length=11, unique=True)
    password:str = ormar.String(max_length=8)
    is_active:bool = ormar.Boolean(default=True)
    is_admin:bool = ormar.Boolean(default=False)
    is_superuser:bool = ormar.Boolean(default=False)

    otp:int = ormar.Integer()
    time_otp = ormar.DateTime()

    class Meta(BaseMeta):
        tablename = 'Users'