import typing

from fastapi import APIRouter, Request, HTTPException
from fastapi.responses import ORJSONResponse

from users.models import User
from permissions.models import Permission


router = APIRouter(
  prefix='/resources',
  tags=['resources'],
)


@router.get('/', response_class=ORJSONResponse)
async def resources(resource_type: str, request: Request):
  email = request.headers.get('x-auth', '').strip()
  user = await User.get_or_none(email=email).prefetch_related('roles')
  if not user:
    raise HTTPException(status_code=401)

  # Get all select resources to which user has access to
  permissions = await Permission.filter(
      role__id__in=[r.pk for r in user.roles], action__name='Read').prefetch_related('resource')
  resp = {}
  duplicate = {}
  index = 0
  for permission in permissions:
    if permission.resource.value in duplicate:
      continue
    if permission.resource.res_type != resource_type:
      continue
    index += 1
    resp[str(index)] = {
      'pk': permission.resource.pk,
      'value': permission.resource.value,
    }
    duplicate[permission.resource.value] = None

  return resp

