from tortoise import fields
from base.models import Base


class Resource(Base):

  value = fields.CharField(max_length=255)
  res_type = fields.CharField(max_length=255)
