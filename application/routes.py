from __future__ import unicode_literals, absolute_import
from collections import OrderedDict, namedtuple
from datetime import datetime

from flask import request, session, g, redirect, url_for, abort, \
        render_template, flash
from flask.ext.login import login_required, current_user

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

@app.errorhandler(403)
def forbidden(e):
    return render_template('403.html')

@app.errorhandler(404)
def not_found(e):
    return render_template('404.html')

@login_manager.unauthorized_handler
def please_login():
    abort(403)

@app.route('/', defaults={'slug': 'index'})
@app.route('/<path:slug>')
def article(slug):
    g.active_page = slug
    article = models.Article.query.get(slug)
    if not article:
        abort(404)
    return render_template('article.html', article=article)

@app.route('/contact')
def contact():
    return 'Sorry, not working yet'

@app.route('/admin/')
@login_required
def admin():
    articles = models.Article.query.all()
    return render_template('admin.html', articles=articles)

@app.route('/admin/new', methods=['GET', 'POST'])
@login_required
def add_article():
    if current_user.email != app.config['WEBMASTER_EMAIL']:
        abort(403)

    if request.method == 'POST':
        article = models.Article(request.form['title'], request.form['content'], request.form['slug'])
        if 'preview' in request.form:
            return render_template('article_form.html', action=url_for('add_article'), preview=True, article=article)
        else:
            g.db.session.add(article)
            g.db.session.commit()
            flash('New article has been recorded.')
            return redirect(url_for('article', slug=article.slug) or url_for('list'))
    else:
        return render_template('article_form.html', action=url_for('add_article'))

@app.route('/admin/edit/<path:slug>', methods=['GET', 'POST'])
@login_required
def edit_article(slug):
    if current_user.email != app.config['WEBMASTER_EMAIL']:
        abort(403)

    article = models.Article.query.get(slug)
    if request.method == 'POST':
        article.slug = request.form['slug']
        article.title = request.form['title']
        article.content = request.form['content']
        if 'preview' in request.form:
            return render_template('article_form.html', article=article, preview=True, action=url_for('edit_article', slug=slug))
        else:
            g.db.session.commit()
            flash('Article edited.')
            return redirect(url_for('article', slug=article.slug))
    else:
        return render_template('article_form.html', article=article, action=url_for('edit_article', slug=slug))

@app.route('/admin/drop/<path:slug>', methods=['GET', 'POST'])
@login_required
def drop_article(slug):
    if current_user.email != app.config['WEBMASTER_EMAIL']:
        abort(403)

    article = models.Article.query.get(slug)
    if request.method == 'POST':
        if 'confirm' in request.form:
            g.db.session.delete(article)
            g.db.session.commit()
        return redirect(url_for('admin'))
    else:
        return render_template('confirm.html', action=url_for('drop_article', slug=slug),
                               query='delete the article titled "%s"' % article.title)
