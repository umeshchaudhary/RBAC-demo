import os
import asyncio
from tortoise import Tortoise, fields
from users.models import User
from roles.models import Role
from action_types.models import ActionType
from resources.models import Resource
from permissions.models import Permission
from settings import MODELS, db_url

from console_interaction_handler import get_options_for_user
from console_interaction_handler import get_roles
from console_interaction_handler import create_user as add_user


async def get_db_connection():
  await Tortoise.init(
    db_url=db_url,
    modules={'models': MODELS}
  )


async def clean_db():
  await User.all().delete()
  await Role.all().delete()
  await Resource.all().delete()
  await ActionType.all().delete()
  await Permission.all().delete()


interaction_handler = {}


async def render_user_roles(user, roles=None):
  print('Please select roles. You comma separated options for multiple roles. For ex: 1,2')
  if not roles:
    roles = await get_roles(user)
  for index, option in roles.items():
    print(f'[{index}] {option["value"]}')
  return roles


async def create_user(user, existing_user=None):
  while True:
    if not existing_user:
      existing_user = {}
      print('Enter name')
      existing_user['name'] = input('=> ').strip()
      print('Enter email')
      existing_user['email'] = input('=> ').strip().lower()
      available_roles = await render_user_roles(user)
      user_input = input('=> ').strip().split(',')
      selected_roles = []
      for role in user_input:
        selected_roles.append(available_roles.get(role.strip())["pk"])
      existing_user['roles'] = selected_roles
    resp = await add_user(user, existing_user)
    if not resp:
      print('Invalid info. Please try again.')
      continue
    print('User create successfully.')
    return resp


async def add_new_roles(user, existing_roles):
  available_roles = await render_user_roles(user)
  user_input = input('=> ').strip().split(',')
  for role in user_input:
    role = role.strip()
    if role in available_roles:
      existing_roles[role] = available_roles[role]


async def remove_existing_roles(user, existing_roles):
  await render_user_roles(user, existing_roles)
  user_input = input('=> ').strip().split(',')
  for role in user_input:
    role = role.strip()
    if role in existing_roles:
      del existing_roles[role]


async def edit_user_role(user):
  save = False
  roles = {}
  email = ''
  while True:
    if not save:
      print('Enter user email for which roles need to be update.')
      email = input('=> ').strip().lower()
      roles = await get_roles(user, email)
      print('List of roles to which user is currently associated.')
      for index, option in roles.items():
        print(f'[{index}] {option["value"]}')
    print('Select an option. Anything other than the available options will send back to the main menu.')
    print('[1] Add new role/roles')
    print('[2] Remove existing role/roles')
    if save:
      print('[3] Save changes')
    user_input = input('=> ').strip()
    save = True
    if user_input == '1':
      await add_new_roles(user, roles)
    elif user_input == '2':
      await remove_existing_roles(user, roles)
    elif user_input == '3':
      role_ids = []
      for k, v in roles.items():
        role_ids.append(v['pk'])
      resp = await create_user(user, {
        'name': '',
        'email': email,
        'roles': role_ids
      })
      if not resp:
        print('Invalid input. Please try again.')
        continue
      print('User roles updated successfully.')
      break
    else:
      break
    print('User roles will be updated as shown below')
    for index, option in roles.items():
      print(f'[{index}] {option["value"]}')


async def view_roles(user):
  roles = await get_roles(user, user)
  print('List of roles to which user is currently associated.')
  for index, option in roles.items():
    print(f'[{index}] {option["value"]}')

  input('Press Enter to continue.')


async def access_resources(user):
  options = await get_options_for_user(user, 'entity')
  print('You have access to the following resources.')
  for index, option in options.items():
    print(f'=> {option["value"]}')

  input('Press Enter to continue...')


async def init_db():

  # Create user roles
  admin_role = await Role.create(name='Admin')
  member_role = await Role.create(name='Member')

  # Create users
  admin_user = await User.create(name='Admin', email='admin1@gmail.com')
  await admin_user.roles.add(*(admin_role,))
  member = await User.create(name='Member', email='member1@gmail.com')
  await member.roles.add(*(member_role,))

  # Create action types
  read_action = await ActionType.create(name='Read')

  resource1 = await Resource.create(value='Login as another user', res_type='select')
  resource2 = await Resource.create(value='Create user', res_type='select')
  resource3 = await Resource.create(value='Edit role', res_type='select')
  resource4 = await Resource.create(value='View roles', res_type='select')
  resource5 = await Resource.create(value='Access resource', res_type='select')
  resource6 = await Resource.create(value='Admin Portal', res_type='entity')
  resource7 = await Resource.create(value='Schedule bookings', res_type='entity')
  resource8 = await Resource.create(value='Manage calendar connection', res_type='entity')

  interaction_handler[resource2.pk] = create_user
  interaction_handler[resource3.pk] = edit_user_role
  interaction_handler[resource4.pk] = view_roles
  interaction_handler[resource5.pk] = access_resources

  await Permission.create(role=admin_role, resource=resource1, action=read_action)
  await Permission.create(role=member_role, resource=resource1, action=read_action)
  await Permission.create(role=admin_role, resource=resource2, action=read_action)
  await Permission.create(role=admin_role, resource=resource3, action=read_action)
  await Permission.create(role=member_role, resource=resource4, action=read_action)
  await Permission.create(role=member_role, resource=resource5, action=read_action)
  await Permission.create(role=admin_role, resource=resource6, action=read_action)
  await Permission.create(role=admin_role, resource=resource7, action=read_action)
  await Permission.create(role=member_role, resource=resource7, action=read_action)
  await Permission.create(role=admin_role, resource=resource8, action=read_action)
  await Permission.create(role=member_role, resource=resource8, action=read_action)


admin_user = 'admin1@gmail.com'


async def start_interaction():
  user = admin_user
  temp_user = None
  while True:
    # get options for a admin user
    option_handlers, user = await render_interactions(user)
    if not option_handlers:
      user = temp_user
      continue
    user_input = input("=> ").strip()
    if user_input == '1':
      temp_user = user
      user = None
      continue
    handler = option_handlers.get(user_input)
    await handler(user)


async def render_interactions(user=None):
  if not user:
    print('Enter user email to login')
    user = input('=> ').strip().lower()
  options = await get_options_for_user(user)
  handlers = {}
  if not options:
    print('Invalid user email. Try again')
    return {}, None
  for index, option in options.items():
    print(f'[{index}] {option["value"]}')
    handlers[f'{index}'] = interaction_handler.get(option['pk'])
  return handlers, user


if __name__ == '__main__':
  loop = asyncio.get_event_loop()

  os.system('rm -rf migrations')
  os.system('aerich init-db')
  # Connect Tortoise ORM to database
  loop.run_until_complete(get_db_connection())
  # loop.run_until_complete(clean_db())
  loop.run_until_complete(init_db())
  try:
    loop.run_until_complete(start_interaction())
  except Exception as ex:
    print(ex.args)
    pass
  finally:
    loop.run_until_complete(Tortoise.close_connections())
    os.system('rm db.sqlite3')
    os.system('rm -rf migrations')


