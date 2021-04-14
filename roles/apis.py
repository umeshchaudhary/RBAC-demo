import typing

from fastapi import APIRouter, Request, HTTPException
from fastapi.responses import ORJSONResponse

from users.models import User
from .models import Role


router = APIRouter(
  prefix='/roles',
  tags=['roles'],
)


@router.get('/', response_class=ORJSONResponse)
async def get_roles(email: typing.Optional[str] = None, request: Request = None):
  login_user_email = request.headers.get('x-auth', '').strip()
  login_user = await User.get_or_none(email=login_user_email).prefetch_related('roles')
  if not login_user:
    raise HTTPException(status_code=401)

  if email:
    user = await User.get_or_none(email=email).prefetch_related('roles')
    roles = user.roles
  else:
    roles = await Role.all()
  resp = {}
  for index, role in enumerate(roles):
    resp[str(index + 1)] = {
      'pk': role.pk,
      'value': role.name,
    }
  return resp
