#!/usr/bin/python
# -*- coding: utf-8 -*-

import json
from bson import ObjectId
from bleach import clean

from flask.ext.login import login_required, login_user, logout_user, current_user
from flask import render_template, redirect, flash, url_for, request, jsonify

from app.helpers.route import RouteHelper
from app.helpers.attachment import AttachmentHelper
from app.models.attachment import AttachType
from . import route_blueprint
from app.helpers.parameter import check_form_para
from app.helpers.category import CategoryHelper
from app.helpers.user import UserHelper
from app.helpers.timestamp import get_formatted_time


@route_blueprint.route('/<route_id>/', methods=['GET'])
@login_required
def route_page(route_id):
    try:
        route_id = ObjectId(route_id)
    except :
        flash('invalid route_id')
        return redirect(url_for('home.home'))
    
    route = RouteHelper.get(route_id)

    route.author = UserHelper.get(route.author)
    route.formatted_time = get_formatted_time(route.create_ts)
    route.stat = RouteHelper.get_route_stat(route.id)
    route.cleaned_content = route.content.read().decode('utf-8')  # TODO: use bleach to sanitise html
    route.my_rate = RouteHelper.get_user_rate(route.id)
    attachs = RouteHelper.get_attachs(route.id)
    joined = route.id in current_user.entered_routes
    finished = RouteHelper.is_route_finished(route.id)

    if not route.finished:
        return redirect(url_for('route.add_attach_page', route_id=route.id))

    return render_template('route-detail.html', route=route, attachs=attachs, joined=joined, finished=finished)


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
        flash('you are not the author of the route')
        return redirect(url_for('home.home'))

    attachs = []
    for attach_id in route.attached:
        attachment = AttachmentHelper.get(ObjectId(attach_id))
        if attachment.atype != AttachType.TEXT.value:
            attachment.info = json.loads(attachment.info)
        attachs.append(attachment)
    
    return render_template('create-attach.html', route=route, attachs=attachs)


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
        flash('you are not the author of the route')
        return redirect(url_for('home.home'))

    try:
        check_form_para(['key', 'type'])
    except AssertionError, e:
        flash(e.message)
        return redirect(url_for('route.add_attach_page', route_id=route.id))

    info_type = AttachType(int(request.form['type']))

    try:
        AttachmentHelper.add(route_id, info_type, request.form['key'])
    except AssertionError, e:
        flash(e.message)
    else:
        flash(u'资料添加成功')

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

    RouteHelper.finish_edit(route.id)

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

    flash(u'删除成功')
    return redirect(url_for('route.add_attach_page', route_id=route.id))


@route_blueprint.route('/category/<category_id>/create_route/', methods=['GET'])
@login_required
def create_route_page(category_id):
    try:
        category_id = ObjectId(category_id)
        assert isinstance(category_id, ObjectId), 'invalid category_id'
        assert CategoryHelper.get(category_id), 'category not found'
    except AssertionError, e:
        flash(e.message)
        return redirect(url_for('home.home'))
    return render_template('create-route.html', category_id=category_id)


@route_blueprint.route('/category/<category_id>/add/', methods=['POST'])
@login_required
def add_route(category_id):
    try:
        category_id = ObjectId(category_id)
        assert len(request.form['title']) > 0, 'please input title'
        assert 'content' in request.form, 'please input route content'
        assert isinstance(category_id, ObjectId)
        cate = CategoryHelper.get(category_id)
        assert cate

        new_route = RouteHelper.add(request.form['title'], cate.id, request.form['content'])
    except AssertionError, e:
        flash(e.message)
        return redirect(url_for('home.home'))

    return redirect(url_for('route.add_attach_page', route_id=new_route.id))


@route_blueprint.route('/join/<route_id>/', methods=['GET'])
@login_required
def join(route_id):
    try:
        route_id = ObjectId(route_id)
        assert RouteHelper.get(route_id)
    except AssertionError, e:
        return redirect(url_for('home.home'))

    RouteHelper.join(route_id)
    return redirect(url_for('route.route_page', route_id=route_id))


@route_blueprint.route('/finish_attach/<route_id>/<attachment_id>/', methods=['GET'])
@login_required
def finish_attach(route_id, attachment_id):
    try:
        route_id = ObjectId(route_id)
        attachment_id = ObjectId(attachment_id)
        assert RouteHelper.get(route_id)
        assert AttachmentHelper.get(attachment_id)
    except AssertionError, e:
        return redirect(url_for('home.home'))

    RouteHelper.finish_attach(route_id, attachment_id)
    return redirect(url_for('route.route_page', route_id=route_id))


@route_blueprint.route('/route/<route_id>/rate/', methods=['POST'])
@login_required
def rate(route_id):
    try:
        route_id = ObjectId(route_id)
        assert 'score' in request.form
        score = int(request.form['score'])
        assert RouteHelper.get(route_id)
    except AssertionError, e:
        return redirect(url_for('home.home'))

    RouteHelper.rate(route_id, score)
    return redirect(url_for('route.route_page', route_id=route_id))


@route_blueprint.route('/route/<route_id>/attach/<attachment_id>/like/', methods=['POST'])
@login_required
def like_attach(route_id, attachment_id):
    try:
        route_id = ObjectId(route_id)
        attachment_id = ObjectId(attachment_id)
        assert RouteHelper.get(route_id)
        assert AttachmentHelper.get(attachment_id)
        state, number = AttachmentHelper.toggle_vote(attachment_id)
    except AssertionError:
        return jsonify({'code': 0})

    return jsonify({'code': state, 'number': number})


@route_blueprint.route('/search/', methods=['GET'])
@login_required
def search():
    try:
        assert 'keywords' in request.args
    except AssertionError, e:
        return redirect(url_for('home.home'))

    results = RouteHelper.search(request.args['keywords'])
    return render_template('search.html', results=results, keywords=request.args['keywords'])
