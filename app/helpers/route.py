from datetime import datetime
from bson import ObjectId
from flask.ext.login import current_user, AnonymousUserMixin
from mongoengine import *

from app.models.user import User
from app.models.route import Route
from app.models.entered_route import EnteredRoute
from app.helpers.timestamp import dt_to_ts
from app.helpers.user import UserHelper
from app.helpers.attachment import AttachmentHelper


class RouteHelper(object):
    @staticmethod
    def get(route_id):
        return Route.objects(id=route_id).first()

    @staticmethod
    def get_all():
        return Route.objects()

    @staticmethod
    def get_entered_route(route_id):
        """Get he EnteredRoute Document"""
        assert isinstance(route_id, ObjectId)
        route = RouteHelper.get(route_id)
        assert route
        
        return EnteredRoute.objects( Q(user=current_user.id) & Q(route=route_id) ).first()

    @staticmethod
    def join(route_id):
        """Join the Route"""
        assert isinstance(route_id, ObjectId)
        route = RouteHelper.get(route_id)
        assert route
        assert route.finished == True

        new_entered_route = EnteredRoute()
        new_entered_route.user = current_user.id
        new_entered_route.route = route_id
        new_entered_route.save()
        
        user = UserHelper.get(current_user.id)
        if route_id not in user.entered_routes:
            user.entered_routes.append(route_id)
        user.save()


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
    def finish_edit(route_id):
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

    @staticmethod
    def finish_attach(route_id, attach_id):
        assert isinstance(route_id, ObjectId)
        assert isinstance(attach_id, ObjectId)
        assert AttachmentHelper.get(attach_id)
        assert RouteHelper.get(route_id)

        route = RouteHelper.get(route_id)
        entered_route = RouteHelper.get_entered_route(route_id)
        assert entered_route
        if attach_id in route.attached and attach_id not in entered_route.attach_complete:
            entered_route.attach_complete.append(attach_id)

        entered_route.percenrage = len(entered_route.attach_complete) / float(route.n_attachment) * 100

        entered_route.save()

    @staticmethod
    def get_stat(finished):
        """Get user's route statistics, True: return finished number, False: return unfinished number, None: return total number"""
        if finished == True:
            return EnteredRoute.objects(Q(user=current_user.id) & Q(percentage=100)).count()
        elif finished == False:
            return EnteredRoute.objects(Q(user=current_user.id) & Q(percentage__ne=100)).count()
        else:
            return EnteredRoute.objects(user=current_user.id).count()

