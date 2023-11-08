from tortoise.models import Model
from tortoise import fields
from tortoise.contrib.pydantic import pydantic_model_creator


class User(Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=255)
    access = fields.CharField(max_length=255)
    email = fields.CharField(max_length=255)
    avatar = fields.CharField(max_length=500)
    created_at = fields.DatetimeField(auto_now_add=True)

    def __str__(self):
        return self.name


UserSchema = pydantic_model_creator(User)
