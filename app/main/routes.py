from app.main import bp
from flask import render_template, current_app, g, flash, redirect, url_for, request
from flask_login import current_user, login_required
from app.models import User, db
from datetime import datetime
from app.main.forms import UploadForm, SearchForm
from app.models import Tool


@bp.before_app_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()
    g.title = current_app.config['SITE_TITLE']


@bp.route('/', methods=['GET', 'POST'])
def index():
    form = SearchForm()
    q = pagination = tools = tool_query = None
    if form.validate_on_submit():
        q = form.q.data
        tool_query = Tool.query.filter(Tool.name.ilike(f'%{q}%'))
        pagination, tools = get_pagination(tool_query)
        if not tools:
            flash('找不到工具，换个关键字试试？', 'danger')
    return render_template('index.html', form=form, pagination=pagination, tools=tools)


@bp.route('/user/<string:username>')
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    tool_query = user.tools
    pagination, tools = get_pagination(tool_query)
    return render_template('user.html', user=user, pagination=pagination, tools=tools)


@bp.route('/upload', methods=['GET', 'POST'])
@login_required
def upload():
    form = UploadForm()
    if form.validate_on_submit():
        tool = Tool(name=form.name.data, url=form.url.data, owner=current_user)
        db.session.add(tool)
        db.session.commit()
        flash('添加成功', 'success')
        return redirect(url_for('main.user', username=current_user.username))
    return render_template('upload.html', form=form)


@bp.route('/all-tools')
def all_tools():
    tool_query = Tool.query
    pagination, tools = get_pagination(tool_query)
    return render_template('all.html', pagination=pagination, tools=tools)


@bp.route('/all-users')
def all_users():
    user_query = User.query
    pagination, users = get_pagination(user_query)
    return render_template('all.html', pagination=pagination, users=users)


@bp.route('/about')
def about():
    return render_template('about.html')


@bp.app_template_global()
def get_pagination(query):
    page = request.args.get('page', 1, type=int)
    pagination = query.paginate(page, per_page=current_app.config['TOOL_PER_PAGE'])
    items = pagination.items
    return pagination, items
