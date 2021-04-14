from fastapi import FastAPI, Request, HTTPException
from tortoise import Tortoise
import logging
import sys
from users.models import User
from settings import MODELS, db_url
from resources.apis import router as resource_apis
from roles.apis import router as role_apis
from users.apis import router as user_apis


fmt = logging.Formatter(
    fmt="%(asctime)s - %(name)s:%(lineno)d - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
sh = logging.StreamHandler(sys.stdout)
sh.setLevel(logging.ERROR)
sh.setFormatter(fmt)

# will print debug sql
logger_db_client = logging.getLogger("db_client")
logger_db_client.setLevel(logging.ERROR)
logger_db_client.addHandler(sh)

logger_tortoise = logging.getLogger("tortoise")
logger_tortoise.setLevel(logging.ERROR)
logger_tortoise.addHandler(sh)

app = FastAPI()

app.include_router(resource_apis)
app.include_router(role_apis)
app.include_router(user_apis)


# @app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    async for obj in User.all():
        print(obj.email)
    email = request.headers.get('x-auth', '').strip()
    user = await User.get_or_none(email=email).prefetch_related('roles')
    if not user:
      raise HTTPException(status_code=401)

    request.headers['x-auth'] = user
    return await call_next(request)


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.on_event("startup")
async def startup():
    print('starting')
    await Tortoise.init(db_url=db_url, modules={"models": MODELS}, use_tz=True)


@app.on_event("shutdown")
async def shutdown():
    print('shutdown')
    await Tortoise.close_connections()


