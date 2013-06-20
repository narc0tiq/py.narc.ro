from __future__ import unicode_literals, absolute_import
from collections import OrderedDict, namedtuple
from datetime import datetime

from flask import request, session, g, redirect, url_for, abort, \
        render_template, flash
from flask.ext.login import login_required

from application import app, models, login_manager

NavbarItem = namedtuple('NavbarItem', ['page_name', 'url', 'title'])
LocalNav = lambda page, title: NavbarItem(page, url_for(page), title)
ArticleNav = lambda article, title: NavbarItem(article, url_for('article', slug=article), title)
RemoteNav = lambda url, title: NavbarItem(None, url, title)

@app.before_request
def start_timer():
    g.start_time = datetime.utcnow()
    g.datetime = datetime

@app.before_request
def setup_navigation():
    g.navbar = models.Sidebar.query.all()

@login_manager.unauthorized_handler
def please_login():
    return render_template('login.html')

@app.route('/', defaults={'slug': 'index'})
@app.route('/<path:slug>')
def article(slug):
    g.active_page = slug
    article = models.Article.query.get(slug)
    return render_template('article.html', article=article)

@app.route('/contact')
def contact():
    return 'Sorry, not working yet'

@app.route('/admin/')
@login_required
def admin():
    articles = models.Article.query.all()
    return render_template('admin.html', articles=articles)

@app.route('/admin/new', methods=['GET'])
@login_required
def new_article():
    return render_template('new_article_form.html')

@app.route('/admin/new', methods=['POST'])
@login_required
def add_article():
    article = models.Article(request.form['title'], request.form['content'], request.form['slug'])
    g.db.session.add(article)
    g.db.session.commit()
    flash('New article has been recorded.')
    return redirect(url_for('article', slug=article.slug) or url_for('list'))

@app.route('/admin/edit/<path:slug>')
@login_required
def edit_article(slug):
    return 'Sorry, not working yet'
