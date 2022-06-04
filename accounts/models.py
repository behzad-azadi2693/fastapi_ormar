import ormar
from config.settings import BaseMeta


class UserModel(ormar.Model):
    id:int = ormar.BigInteger(primary_key=True)
    phonenumber:str = ormar.String(min_length=10, max_length=13, unique=True)
    is_active:bool = ormar.Boolean(default=True)
    is_admin:bool = ormar.Boolean(default=False)
    is_superuser:bool = ormar.Boolean(default=False)

    otp:int = ormar.Integer(nullable=True)
    time_otp = ormar.DateTime(nullable=True)

    class Meta(BaseMeta):
        tablename = 'Users'
