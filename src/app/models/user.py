from tortoise import models, fields
from tortoise.contrib.pydantic import pydantic_model_creator


class User(models.Model):
    id = fields.IntField(pk=True)
    full_name = fields.CharField(100, index=True, null=True)
    email = fields.CharField(100, unique=True, index=True, null=False)
    password_hash = fields.CharField(128, null=True)
    is_active = fields.BooleanField(default=True)
    is_superuser = fields.BooleanField(default=False)

    class PydanticMeta:
        exclude = ["password_hash"]


UserPydantic = pydantic_model_creator(User, name="User")
