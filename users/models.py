from tortoise import fields
from base.models import Base


class User(Base):

  name = fields.CharField(max_length=255)
  email = fields.CharField(max_length=255)
  roles = fields.ManyToManyField('models.Role',
                                 related_name='users',
                                 through='user_role')
