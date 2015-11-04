from datetime import datetime
from bson import ObjectId
from json import loads
from flask.ext.login import current_user, AnonymousUserMixin
from mongoengine import *
from app.models.route import Route, RateInfo
from app.models.entered_route import EnteredRoute
from app.models.category import Category
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
        """Get the EnteredRoute Document"""
        assert isinstance(route_id, ObjectId)
        route = RouteHelper.get(route_id)
        assert route

        return EnteredRoute.objects(Q(user=current_user.id) & Q(route=route_id)).first()

    @staticmethod
    def search(keywords):
        """Search routes by title"""
        assert isinstance(keywords, basestring)
        return list(Route.objects(title__contains=keywords))

    @staticmethod
    def get_attachs(route_id):
        assert isinstance(route_id, ObjectId)
        route = RouteHelper.get(route_id)
        assert route

        attachs = [AttachmentHelper.get(attach_id) for attach_id in route.attached]
        for attach in attachs:
            attach.json_info = loads(attach.info) if attach.atype != 3 else attach.info
            attach.finished = RouteHelper.is_attach_finished(route_id, attach.id)
            attach.n_like = len(attach.upvote_list)
            attach.user_upvoted = current_user.id in attach.upvote_list
        return attachs

    @staticmethod
    def remove_unfinished_route(route_list):
        for route in route_list:
            if isinstance(route, dict):
                if not route['route'].finished:
                    route_list.remove(route)
            elif not route.finished:
                route_list.remove(route)

        return route_list

    @staticmethod
    def join(route_id):
        """Join the Route"""
        assert isinstance(route_id, ObjectId)
        route = RouteHelper.get(route_id)
        assert route
        assert not EnteredRoute.objects(Q(user=current_user.id) & Q(route=route.id))
        assert route.finished

        new_entered_route = EnteredRoute()
        new_entered_route.user = current_user.id
        new_entered_route.route = route_id
        new_entered_route.save()

        user = UserHelper.get(current_user.id)
        if route_id not in user.entered_routes:
            user.entered_routes.append(route_id)
        user.save()

    @staticmethod
    def add(title, father, text):
        assert not isinstance(current_user, AnonymousUserMixin), 'user has not logged in'
        assert isinstance(title, basestring), 'name is not string'
        assert len(title) >= 5, 'route name too short!'
        assert father is None or isinstance(father, ObjectId), 'father is not not valid category id'

        new_route = Route()
        new_route.title = title
        new_route.author = current_user.id
        new_route.create_ts = dt_to_ts(datetime.utcnow())
        if father:
            new_route.father = father

        new_route.content.new_file()
        new_route.content.write(text.encode('utf-8'))
        new_route.content.close()

        new_route.save()

        # add id of new route to father's routes list
        from app.helpers.category import CategoryHelper
        CategoryHelper.add_route(father, new_route.id)

        return new_route

    @staticmethod
    def finish_edit(route_id):
        assert isinstance(route_id, ObjectId)
        route = RouteHelper.get(route_id)
        assert route
        assert not route.finished

        route.finished = True
        route.n_attachment = len(route.attached)
        route.save()
        return route

    @staticmethod
    def clear(route_id):
        from app.helpers.route import RouteHelper
        assert isinstance(route_id, ObjectId)
        route = RouteHelper.get(route_id)
        assert route
        assert not route.finished

        for attach_id in route.attached:
            AttachmentHelper.delete(attach_id)

        while len(route.attached) > 0:
            route.attached.pop()

        route.save()

    @staticmethod
    def delete_route(route_id):
        assert isinstance(route_id, ObjectId)
        route = RouteHelper.get(route_id)
        assert route

        for attach_id in route.attached:
            AttachmentHelper.delete(attach_id)

        f_cate = Category.objects(id=route.father).first()
        f_cate.routes.remove(route.id)
        f_cate.save()

        enters = EnteredRoute.objects(route=route.id)
        for entered_route in enters:
            user = UserHelper.get(entered_route.user)
            user.entered_routes.remove(route.id)
            user.save()
        enters.delete()

        RateInfo.objects(route=route.id).delete()

        route.delete()

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

        entered_route.percentage = len(entered_route.attach_complete) / float(route.n_attachment) * 100

        entered_route.save()

    @staticmethod
    def is_attach_finished(route_id, attach_id):
        assert isinstance(route_id, ObjectId)
        assert isinstance(attach_id, ObjectId)
        assert AttachmentHelper.get(attach_id)
        assert RouteHelper.get(route_id)

        route = RouteHelper.get(route_id)
        entered_route = RouteHelper.get_entered_route(route_id)

        if not entered_route:
            return False

        return attach_id in entered_route.attach_complete

    @staticmethod
    def is_route_finished(route_id):
        assert isinstance(route_id, ObjectId)
        assert RouteHelper.get(route_id)

        route = RouteHelper.get(route_id)
        entered_route = RouteHelper.get_entered_route(route_id)

        if not entered_route:
            return False

        return entered_route.percentage == 100

    @staticmethod
    def get_route_stat(route_id):
        assert isinstance(route_id, ObjectId)
        route = RouteHelper.get(route_id)
        assert route

        stat = dict()
        stat['n_joined'] = EnteredRoute.objects(route=route.id).count()
        stat['n_completed'] = EnteredRoute.objects(Q(route=route.id) & Q(percentage=100)).count()
        stat['n_rate'] = RateInfo.objects(route=route.id).count()

        return stat

    @staticmethod
    def _recalculate_avg(route_id):
        assert isinstance(route_id, ObjectId)
        route = RouteHelper.get(route_id)
        assert route

        route.avg_rate = RateInfo.objects(route=route.id).average('score')
        route.save()

    @staticmethod
    def rate(route_id, score):
        assert isinstance(route_id, ObjectId)
        route = RouteHelper.get(route_id)
        assert route
        assert isinstance(score, int)

        rate_info = RateInfo.objects(Q(route=route_id) & Q(user=current_user.id)).first()
        if rate_info:
            rate_info.score = score
            rate_info.save()
        else:
            rate_info = RateInfo()
            rate_info.route = route_id
            rate_info.user = current_user.id
            rate_info.score = score
            rate_info.save()

        RouteHelper._recalculate_avg(route_id)

    @staticmethod
    def get_user_rate(route_id):
        assert isinstance(route_id, ObjectId)
        route = RouteHelper.get(route_id)
        assert route

        rate_info = RateInfo.objects(Q(route=route_id) & Q(user=current_user.id)).first()

        if rate_info:
            return rate_info.score
        else:
            return None

    @staticmethod
    def get_user_routes(finished):
        assert isinstance(finished, bool)

        if finished:
            entered_routes = list(EnteredRoute.objects(Q(user=current_user.id) & Q(percentage=100)))
        else:
            entered_routes = list(EnteredRoute.objects(Q(user=current_user.id) & Q(percentage__ne=100)))

        routes = []
        for entered in entered_routes:
            routes.append(RouteHelper.get(entered.route))

        if not finished:
            for route in routes:
                route.percentage = RouteHelper.get_entered_route(route.id).percentage

        return routes

    @staticmethod
    def get_user_create_routes():
        return list(Route.objects(author=current_user.id))
