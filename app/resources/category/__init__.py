from flask import Blueprint

__all__ = [
    'category_blueprint'
]

category_blueprint = Blueprint('category', __name__)

import category

