from bson import ObjectId

from flask.ext.login import login_required, login_user, logout_user
from flask import render_template, redirect, flash, url_for, request
from flask.ext.misaka import markdown

from app.helpers.route import RouteHelper
from . import route_blueprint


@route_blueprint.route('/<route_id>/', methods=['GET'])
def get_page(route_id):
    try:
        route_id = ObjectId(route_id)
    except :
        flash('invalid route_id')
        return redirect(url_for('home.home'))
    
    route = RouteHelper.get(route_id)

    return render_template('route.html', route=route)


@route_blueprint.route('/add/', methods=['POST'])
def add_route():
    try:
        assert len(request.form['title']) > 0, 'please input title'
        assert 'md_file' in request.files, 'please select a md file'
    except AssertionError, e:
        flash(e.message)
        return redirect(url_for('home.home'))

    new_route = RouteHelper.add(request.form['title'], None, request.files['md_file'])

    return redirect(url_for('route.get_page', route_id=new_route.id))

