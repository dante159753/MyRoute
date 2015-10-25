from datetime import datetime
from bson import ObjectId
from flask.ext.login import current_user, AnonymousUserMixin

from app.models.user import User
from app.models.route import Route
from app.helpers.timestamp import dt_to_ts


class RouteHelper(object):
    @staticmethod
    def get(route_id):
        return Route.objects(id=route_id).first()

    @staticmethod
    def get_all():
        return Route.objects()

    @staticmethod
    def add(title, father, mdtext):
        assert not isinstance(current_user, AnonymousUserMixin), 'user has not logged in'
        assert isinstance(title, basestring), 'name is not string'
        assert len(title) >= 5, 'route name too short!'
        assert father == None or isinstance(father, Route), 'father is not Route'

        new_route = Route()
        new_route.title = title
        new_route.author = current_user.id
        new_route.create_ts = dt_to_ts(datetime.utcnow())

        new_route.md_file.new_file()
        new_route.md_file.write(mdtext.encode('utf-8'))
        new_route.md_file.close()

        new_route.save()
        return new_route

    @staticmethod
    def finish(route_id):
        assert isinstance(route_id, ObjectId)
        route = RouteHelper.get(route_id)
        assert route
        assert route.finished == False

        route.finished = True
        route.n_attachment = len(route.attached)
        route.save()
        return route

    @staticmethod
    def clear(route_id):
        assert isinstance(route_id, ObjectId)
        route = RouteHelper.get(route_id)
        assert route
        assert route.finished == False
        
        from app.helpers.route import RouteHelper
        for attach_id in route.attached:
            AttachmentHelper.delete(attach_id)

        while len(route.attached) > 0:
            route.attached.pop()

        route.save()

    @staticmethod
    def modify(route_id, mdfile):
        assert allowed_file(mdfile.filename), 'invalid filename'

        route = Route.objects(id=route_id)
        route.md_file.replace(mdfile)

        return route

