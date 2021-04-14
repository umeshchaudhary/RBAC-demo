from tortoise.models import Model
from tortoise import fields


class Base(Model):
    # Defining `id` field is optional, it will be defined automatically
    # if you haven't done it yourself
    created_on = fields.DatetimeField(auto_now_add=True)
    updated_on = fields.DatetimeField(auto_now=True)

