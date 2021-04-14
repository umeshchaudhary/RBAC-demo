# Auth Service

Auth service is a role based access control system that manages the user permissions more effectively.

Major tools and modules used are
- Python3.8
- FastAPI (async  API framework)
- Tortoise (async ORM)


## Major files and modules to look for

- users
 -> apis
 -> models
- settings.py
- console_interaction_handler.py
- console.py
- permissions
- resources
- roles


## Intention

The application is designed as a microservice which can run on any port and serve the customers. I choose this approch because creating a microservice from scrach is quite easy as there are a lot of tools available which automates the process. I used the api endpoints as the main service for the console application.

## Database Structure

There are 4 major models
- User (name, email)
- Role (name)
- Resource (name, type)
- ActionType (name)

There two mapping models
- UserRoleMapping (user_id, role_id)
- RoleResourceActionMapping (role_id, Resource_id, action_id)


## Data Flow

1. we execute the `console.py` file.
2. It first creates the initial data within the in-memory db.
3. Choose a user email which was created as admin in previous step.
4. Get the interaction options for that user
    * call the actual application API using TestClient with user email as X-Auth in headers.
    * The API then picks up that header value and tries to find the user.
    * Get the relavant dat and return it to the  test client as response.


## Application setup

- Create a virtualenv `python3 -m venv venv`
- Active the environment `source venv/bin/active`
- Install all requirements `pip install -r requirements.txt`
- Execute the python script `python console.py`