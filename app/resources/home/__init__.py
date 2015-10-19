from flask import Blueprint
from flask_restful import Api

__all__ = [
    'home_blueprint'
]

home_blueprint = Blueprint('home', __name__)

import home

