from tortoise import fields
from base.models import Base


class Role(Base):

  name = fields.CharField(max_length=255)
