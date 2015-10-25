import hashlib
import binascii
import os

from app.models.user import User
from app.app import login_manager


@login_manager.user_loader
def user_loader(user_id):
    """Given *user_id*, return the associated User object.

    :param unicode user_id: user_id (email) user to retrieve
    """
    return User.objects(email=user_id).first()


@login_manager.unauthorized_handler
def unauthorized_redirect():
    return redirect(url_for('home.home'))


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
    def get_by_email(email):
        assert isinstance(email, basestring)

        return User.objects(email=email).first()

    @staticmethod
    def create_user(nickname, email, password, gender):
        """Sign up a user"""

        # check wheather the email has been registered
        assert UserHelper.get_by_email(email) == None

        assert isinstance(nickname, basestring)
        assert isinstance(email, basestring)
        assert isinstance(password, basestring)
        assert gender in [0,1]

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
        

