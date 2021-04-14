

from httpx import AsyncClient

from main import app


async def get_options_for_user(user, resource_type='select'):
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get(f"/resources?resource_type={resource_type}", headers={"X-Auth": user})
    if response.status_code != 200:
      return None
    return response.json()


async def get_roles(user, email=None):
  url = "/roles"
  if email:
    url += "?email=" + email
  async with AsyncClient(app=app, base_url="http://test") as ac:
    response = await ac.get(url, headers={"X-Auth": user})
  if response.status_code != 200:
    return None
  return response.json()


async def create_user(user, new_user):
  async with AsyncClient(app=app, base_url="http://test") as ac:
    response = await ac.post("/users", headers={"X-Auth": user}, json=new_user)
  if response.status_code != 200:
    return None
  return response.json()
