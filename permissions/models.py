from tortoise import fields
from base.models import Base


class Permission(Base):

  role = fields.ForeignKeyField(model_name='models.Role')
  resource = fields.ForeignKeyField(model_name='models.Resource', related_name='permissions')
  action = fields.ForeignKeyField(model_name='models.ActionType')

