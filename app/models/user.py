from mongoengine import *
from flask.ext.login import UserMixin


__all__ = ['User']


class User(Document, UserMixin):
    nickname = StringField(required=True)
    email = EmailField(required=True)
    salted_password = StringField(required=True)
    salt = StringField(required=True)
    gender = IntField(required=True, choices=[0,1])
    point = IntField(default=0)
    entered_routes = ListField(ObjectIdField())

    def is_active(self):
        """True, as all users are active."""
        return True

    def get_id(self):
        """Return the email address to satisfy Flask-Login's requirements."""
        return self.email

    def is_authenticated(self):
        """Return True if the user is authenticated."""
        return True

    def is_anonymous(self):
        """False, as anonymous users aren't supported."""
        return False

