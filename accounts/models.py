import ormar
from config.settings import BaseMeta


class UserModel(ormar.Model):
    id:int = ormar.BigInteger(primary_key=True)
    phonenumber:int = ormar.Integer(unique=True)
    is_active:bool = ormar.Boolean(default=False)
    is_admin:bool = ormar.Boolean(default=False)
    is_superuser:bool = ormar.Boolean(default=False)

    otp:int = ormar.Integer()
    time_otp = ormar.DateTime()

    class Meta(BaseMeta):
        tablename = 'Users'
