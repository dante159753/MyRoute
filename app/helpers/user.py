import hashlib
import binascii
import os
from base64 import b64encode
from bson import ObjectId
from flask import redirect, url_for
from flask.ext.login import current_user
from mongoengine import *
from app.models.user import User
from app.models.entered_route import EnteredRoute
from app.app import login_manager


@login_manager.user_loader
def user_loader(user_id):
    """Given *user_id*, return the associated User object.

    :param unicode user_id: user_id (email) user to retrieve
    """
    return User.objects(email=user_id).first()


@login_manager.unauthorized_handler
def unauthorized_redirect():
    return redirect(url_for('home.intro'))

ALLOWED_EXTENSIONS = set(['jpg', 'jpeg'])


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


class UserHelper(object):
    @staticmethod
    def _password_hash(password, salt):
        """Calculate password hash.

        :param password: original password
        :param salt: salt string
        :return: hashed password
        """
        return hashlib.sha256(password + salt).hexdigest()

    @staticmethod
    def verify_password(user, password):
        """Verify user password."""
        assert isinstance(user, User)
        assert isinstance(password, basestring)

        return user.salted_password == UserHelper._password_hash(password, user.salt)

    @staticmethod
    def get(user_id):
        assert isinstance(user_id, ObjectId)
        return User.objects(id=user_id).first()

    @staticmethod
    def get_by_email(email):
        assert isinstance(email, basestring)

        return User.objects(email=email).first()

    @staticmethod
    def create_user(nickname, email, password, gender):
        """Sign up a user"""

        # check weather the email has been registered
        assert UserHelper.get_by_email(email) is None

        assert isinstance(nickname, basestring)
        assert isinstance(email, basestring)
        assert isinstance(password, basestring)
        assert gender in [0, 1]

        # Prepare password
        salt = binascii.hexlify(os.urandom(32))
        salted_password = UserHelper._password_hash(password, salt)

        new_user = User()
        new_user.nickname = nickname
        new_user.email = email
        new_user.salt = salt
        new_user.salted_password = salted_password
        new_user.gender = gender
        new_user.save()

        return new_user

    @staticmethod
    def modify_password(new_password):
        assert isinstance(new_password, basestring)
        user = UserHelper.get(current_user.id)

        salt = binascii.hexlify(os.urandom(32))
        salted_password = UserHelper._password_hash(new_password, salt)

        user.salt = salt
        user.salted_password = salted_password
        user.save()

        return user

    @staticmethod
    def modify_avatar(img):
        assert img and allowed_file(img.filename)

        encoded = b64encode(img.read())

        user = UserHelper.get(current_user.id)

        user.avatar.new_file()
        user.avatar.write(encoded)
        user.avatar.close()

        user.save()

        return user

    @staticmethod
    def get_stat(finished):
        """
        Get user's route statistics.

        True: return finished number,
        False: return unfinished number,
        None: return total number

        """
        if finished == True:
            return EnteredRoute.objects(Q(user=current_user.id) & Q(percentage=100)).count()
        elif finished == False:
            return EnteredRoute.objects(Q(user=current_user.id) & Q(percentage__ne=100)).count()
        else:
            return EnteredRoute.objects(user=current_user.id).count()

