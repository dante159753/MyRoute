from flask import Blueprint
from flask_restful import Api

__all__ = [
    'blueprint'
]

blueprint = Blueprint('user', __name__)
api = Api(blueprint)


from .account import LoginRes, LogoutRes, RegisterRes
#from .user_home import UserHomeRes
#from .user_info import UserInfoRes
api.add_resource(LoginRes, '/login/')
api.add_resource(LogoutRes, '/logout/')
api.add_resource(ResgisterRes, '/user/register/')
#api.add_resource(UserHomeRes, '/user/home/')
#api.add_resource(UserInfoRes, '/user/info/')
#del LoginRes, LogoutRes, RegisterRes, UserHomeRes, UserInfoRes
del LoginRes, LogoutRes, ResgisterRes


