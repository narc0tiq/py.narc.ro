from __future__ import unicode_literals, absolute_import
from collections import OrderedDict, namedtuple

from flask import request, session, g, redirect, url_for, abort, \
        render_template, flash

from application import app, models

NavbarItem = namedtuple('NavbarItem', ['page_name', 'url', 'title'])
LocalNav = lambda page, title: NavbarItem(page, url_for(page), title)
RemoteNav = lambda url, title: NavbarItem(None, url, title)

@app.before_request
def setup_navigation():
    g.navbar = [
        ('Navigation', [LocalNav('index', "Index"),
                        LocalNav('list', "Articles")]),
        ('Related Sites', [RemoteNav('http://wiki.narc.ro/', "NarcWiki")])]

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/<path:slug>')
def article(slug):
    article = models.Article.query.get(slug)
    return render_template('article.html', article=article)

@app.route('/list')
def list():
    articles = models.Article.query.all()
    return render_template('article_list.html', articles=articles)

@app.route('/admin/')
def admin():
    return render_template('admin.html')

@app.route('/admin/new', methods=['GET'])
def new_article():
    return render_template('new_article_form.html')

@app.route('/admin/new', methods=['POST'])
def add_article():
    article = models.Article(request.form['title'], request.form['content'], request.form['slug'])
    g.db.session.add(article)
    g.db.session.commit()
    flash('New article has been recorded.')
    return redirect(url_for('list'))

