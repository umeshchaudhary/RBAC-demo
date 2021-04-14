MODELS = [
    "users.models",
    "roles.models",
    "resources.models",
    "action_types.models",
    "permissions.models",
    "aerich.models"
]

db_url = "sqlite://db.sqlite3"

TORTOISE_ORM = {
    "connections": {"default": db_url},
    "apps": {
        "models": {
            "models": MODELS,
            "default_connection": "default",
        },
    },
}