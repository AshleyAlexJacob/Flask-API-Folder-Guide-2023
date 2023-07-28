from flask import Blueprint
from src.controllers.user_controller import users

# main blueprint to be registered with application
api = Blueprint('api', __name__)

# register user with api blueprint
api.register_blueprint(users, url_prefix="/users")
