import json
from bson import ObjectId

from flask.ext.login import login_required, login_user, logout_user, current_user
from flask import render_template, redirect, flash, url_for, request
from flask.ext.misaka import markdown

from app.helpers.route import RouteHelper
from app.helpers.attachment import AttachmentHelper
from app.helpers.category import CategoryHelper
from app.models.attachment import AttachType
from . import category_blueprint
from app.helpers.parameter import check_form_para


@category_blueprint.route('/root/', methods=['GET'])
@login_required
def root_page():
    roots = CategoryHelper.get_roots()
    for root in roots:
        root.top_sons = CategoryHelper.get_son_categorys(root.id)[:3]

    return render_template('category.html', roots=roots)


@category_blueprint.route('/<category_id>/', methods=['GET'])
@login_required
def category_page(category_id):
    try:
        category_id = ObjectId(category_id)
        assert CategoryHelper.get(category_id)
    except :
        flash('invalid route_id')
        return redirect(url_for('home.home'))
    
    category = CategoryHelper.get(category_id)
    category.n_routes = len(category.routes)
    breadcrumb_list = [(category.title, category.id)]
    CategoryHelper.gene_bread(breadcrumb_list)

    son_routes = []
    sons_hot_routes = []

    return render_template('route-father.html', breadcrumb_list=breadcrumb_list, category=category, son_routes=son_routes, sons_hot_routes=sons_hot_routes)


@category_blueprint.route('/<route_id>/add_attach/', methods=['GET'])
@login_required
def add_attach_page(route_id):
    try:
        route_id = ObjectId(route_id)
        assert RouteHelper.get(route_id)
        assert not RouteHelper.get(route_id).finished
    except :
        flash('invalid route_id')
        return redirect(url_for('home.home'))

    route = RouteHelper.get(route_id)

    if route.author != current_user.id:
        flash('you are not author of the route')
        return redirect(url_for('home.home'))

    attachs = []
    for attach_id in route.attached:
        attachment = AttachmentHelper.get(ObjectId(attach_id))
        if attachment.atype != AttachType.TEXT.value:
            attachment.info = json.loads(attachment.info)
        attachs.append(attachment)
    
    return render_template('create_route.html', route=route, attachs=attachs)


