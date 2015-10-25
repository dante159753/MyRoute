import json
from bson import ObjectId

from flask.ext.login import login_required, login_user, logout_user, current_user
from flask import render_template, redirect, flash, url_for, request
from flask.ext.misaka import markdown

from app.helpers.route import RouteHelper
from app.helpers.attachment import AttachmentHelper
from app.models.attachment import AttachType
from . import route_blueprint
from app.helpers.parameter import check_form_para


@route_blueprint.route('/<route_id>/', methods=['GET'])
@login_required
def route_page(route_id):
    try:
        route_id = ObjectId(route_id)
    except :
        flash('invalid route_id')
        return redirect(url_for('home.home'))
    
    route = RouteHelper.get(route_id)

    if not route.finished:
        return redirect(url_for('route.add_attach_page', route_id=route.id))

    return render_template('route.html', route=route)


@route_blueprint.route('/<route_id>/add_attach/', methods=['GET'])
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


@route_blueprint.route('/<route_id>/add_attach/', methods=['POST'])
@login_required
def add_attach(route_id):
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

    try:
        check_form_para(['key', 'type'])
    except AssertionError, e:
        flash('wrong para')
        return redirect(url_for('route.add_attach_page', route_id=route.id))

    info_type = AttachType(int(request.form['type']))

    AttachmentHelper.add(route_id, info_type, request.form['key'])

    flash('added successfully')
    return redirect(url_for('route.add_attach_page', route_id=route_id))


@route_blueprint.route('/<route_id>/finish/', methods=['POST'])
@login_required
def finish_edit(route_id):
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

    RouteHelper.finish(route.id)
    
    flash('finished successfully')
    return redirect(url_for('route.route_page', route_id=route.id))


@route_blueprint.route('/<route_id>/attachment/<attach_id>/delete/', methods=['POST'])
@login_required
def delete_attach(route_id, attach_id):
    try:
        route_id = ObjectId(route_id)
        attach_id = ObjectId(attach_id)
        assert RouteHelper.get(route_id)
        assert AttachmentHelper.get(attach_id)
        assert not RouteHelper.get(route_id).finished
    except :
        flash('invalid route_id or attach_id')
        return redirect(url_for('home.home'))

    route = RouteHelper.get(route_id)
    
    if route.author != current_user.id:
        flash('you are not author of the route')
        return redirect(url_for('home.home'))

    AttachmentHelper.delete(attach_id)

    flash('deleted successfully')
    return redirect(url_for('route.add_attach_page', route_id=route.id))


@route_blueprint.route('/add/', methods=['POST'])
@login_required
def add_route():
    try:
        assert len(request.form['title']) > 0, 'please input title'
        assert 'md_text' in request.form, 'please input route content'
    except AssertionError, e:
        flash(e.message)
        return redirect(url_for('home.home'))

    new_route = RouteHelper.add(request.form['title'], None, request.form['md_text'])

    return redirect(url_for('route.add_attach_page', route_id=new_route.id))

@route_blueprint.route('/route/<route_id>/rate/', methods=['POST'])
@login_required
def rate():
    pass

