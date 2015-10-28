import pytz

from base64 import b64encode
from datetime import datetime
from bson import ObjectId
from app.models.category import Category
from app.models.route import RateInfo
from app.helpers.route import RouteHelper
from app.helpers.timestamp import get_formatted_time


class CategoryHelper(object):
    @staticmethod
    def get(category_id):
        return Category.objects(id=category_id).first()

    @staticmethod
    def get_by_title(title):
        return Category.objects(title__startswith=title).first()

    @staticmethod
    def get_roots():
        return Category.objects(father__exists=False)

    @staticmethod
    def gene_bread(bread_list):
        category_id = bread_list[0][1]
        category = CategoryHelper.get(category_id)
        if category.father:
            father_id = category.father
            father = CategoryHelper.get(father_id)
            bread_list.insert(0, (father.title, father.id))
            CategoryHelper.gene_bread(bread_list)

    @staticmethod
    def get_son_categorys(category_id):
        assert isinstance(category_id, ObjectId)
        assert CategoryHelper.get(category_id)

        category = CategoryHelper.get(category_id)

        result_list = []
        for son_category_id in category.sons:
            result_list.append(CategoryHelper.get(son_category_id))

        return result_list

    @staticmethod
    def get_son_routes(category_id):
        assert isinstance(category_id, ObjectId)
        assert CategoryHelper.get(category_id)

        category = CategoryHelper.get(category_id)

        result_list = []
        for son_route_id in category.routes:
            result_list.append(RouteHelper.get(son_route_id))

        for son_route in result_list:
            son_route.formatted_date = get_formatted_time(son_route.create_ts)
            son_route.n_comment = 0 #TODO use disqus api to get comment count
            son_route.n_rate = RateInfo.objects(route=son_route.id).count()

        return result_list

    @staticmethod
    def _reduce_find_hot_route(x, y):
        """ Give x and y, select a hotter one."""
        return x if x > y else y

    @staticmethod
    def _recursive_find_hot_route(category_id):
        """ Give a category, find the hotest route in its routes and sons."""
        category = CategoryHelper.get(category_id)

        hot_route = None
        if category.routes:
            hot_route = reduce(CategoryHelper._reduce_find_hot_route, category.routes)
        if category.sons:
            hot_route = reduce(CategoryHelper._reduce_find_hot_route,
                               [CategoryHelper._recursive_find_hot_route(son_category) for son_category in
                                category.sons], hot_route)

        return hot_route

    @staticmethod
    def get_child_hot_route(category_id):
        """ Give a catetory, find the hotest route in its sons."""
        assert isinstance(category_id, ObjectId)
        assert CategoryHelper.get(category_id)

        category = CategoryHelper.get(category_id)

        hot_route = None
        if category.sons:
            hot_route = reduce(CategoryHelper._reduce_find_hot_route,
                               [CategoryHelper._recursive_find_hot_route(son_category) for son_category in
                                category.sons], hot_route)

        return hot_route

    @staticmethod
    def get_hot_categorys():
        return Category.objects()[:6]

    @staticmethod
    def add(title, desc, father, icon):
        assert isinstance(title, basestring), 'title is not string'
        assert isinstance(desc, basestring), 'title is not string'
        assert len(title) > 0, 'title name too short!'
        assert len(desc) > 5, 'desc name too short!'
        assert father is None or isinstance(father, ObjectId)
        if father:
            assert CategoryHelper.get(father)

        new_category = Category()
        new_category.title = title
        new_category.desc = desc
        if father:
            new_category.father = father
        if icon:
            encoded = b64encode(icon.read())
            new_category.icon.new_file()
            new_category.icon.write(encoded)
            new_category.icon.close()

        new_category.save()

        if father:
            CategoryHelper.add_son(father, new_category.id)

        return new_category

    @staticmethod
    def add_son(category_id, son_category):
        assert isinstance(category_id, ObjectId)
        assert isinstance(son_category, ObjectId)

        assert CategoryHelper.get(son_category), 'invalid son category'

        category = CategoryHelper.get(category_id)
        assert category, 'invalid father category'

        category.sons.append(son_category)
        category.sons = list(set(category.sons))
        category.save()

        return category

    @staticmethod
    def add_route(category_id, route_id):
        assert isinstance(category_id, ObjectId)
        assert CategoryHelper.get(category_id)
        assert isinstance(route_id, ObjectId)
        assert RouteHelper.get(route_id)

        category = CategoryHelper.get(category_id)

        category.routes.append(route_id)
        category.routes = list(set(category.routes))
        category.save()

        return category
