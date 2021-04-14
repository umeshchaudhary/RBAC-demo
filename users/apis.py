import typing
from fastapi import APIRouter, Request, HTTPException
from fastapi.responses import ORJSONResponse
from pydantic import BaseModel

from permissions.models import Permission
from roles.models import Role

from .models import User


router = APIRouter(
  prefix='/users',
  tags=['users'],
)


class UserIn(BaseModel):
  name: str
  email: str
  roles: typing.List[str] = []


@router.post('/', response_class=ORJSONResponse)
async def create_user(user: UserIn, request: Request):
  email = request.headers.get('x-auth', '').strip()
  logged_in_user = await User.get_or_none(email=email).prefetch_related('roles')
  if not logged_in_user:
    raise HTTPException(status_code=401)

  roles = await Role.filter(pk__in=user.roles).distinct()
  if len(roles) != len(user.roles):
    raise HTTPException(status_code=400)

  existing_user = await User.get_or_none(email=user.email)
  if not existing_user:
    existing_user = await User.create(name=user.name, email=user.email)

  await existing_user.roles.clear()
  for role in roles:
    await existing_user.roles.add(role)
  await existing_user.save()
  return {"success": True}
