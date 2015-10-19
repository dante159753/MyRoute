from flask import Blueprint
from flask_restful import Api

__all__ = [
    'user_blueprint'
]

user_blueprint = Blueprint('user', __name__)

import account

