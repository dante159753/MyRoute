from flask import Blueprint
from flask_restful import Api

__all__ = [
    'route_blueprint'
]

route_blueprint = Blueprint('route', __name__)

import route


