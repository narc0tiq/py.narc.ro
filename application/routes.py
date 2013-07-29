from __future__ import unicode_literals, absolute_import
from collections import OrderedDict, namedtuple
from functools import wraps

from flask import request, session, g, redirect, url_for, abort, \
        render_template, flash, Response
from flask.ext.login import login_required, current_user
from flask_mail import Message

from application import app, models, login_manager, mail

NavbarItem = namedtuple('NavbarItem', ['page_name', 'url', 'title'])
LocalNav = lambda page, title: NavbarItem(page, url_for(page), title)
ArticleNav = lambda article, title: NavbarItem(article, url_for('article', slug=article), title)
RemoteNav = lambda url, title: NavbarItem(None, url, title)

def only_admin(function):
    @wraps(function)
    def decorated(*args, **kwargs):
        if current_user.email != app.config['WEBMASTER_EMAIL']:
            abort(403)
        return function(*args, **kwargs)
    return decorated

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

@app.route('/admin/')
@login_required
def admin():
    articles = models.Article.query.all()
    downloads = models.DownloadHit.query.all()
    return render_template('admin.html', articles=articles, downloads=downloads)

@app.route('/admin/new', methods=['GET', 'POST'])
@login_required
@only_admin
def add_article():
    if request.method == 'POST':
        article = models.Article(request.form['title'], request.form['content'], request.form['slug'])
        if 'preview' in request.form:
            flash('Remember this is just a preview: the article has not yet been saved.')
            return render_template('article_form.html', action=url_for('add_article'), preview=True, article=article)
        else:
            g.db.session.add(article)
            g.db.session.commit()
            flash('Article has been saved.')
            return redirect(url_for('article', slug=article.slug) or url_for('list'))
    else:
        return render_template('article_form.html', action=url_for('add_article'))

@app.route('/admin/edit/<path:slug>', methods=['GET', 'POST'])
@login_required
@only_admin
def edit_article(slug):
    article = models.Article.query.get(slug)
    if request.method == 'POST':
        article.slug = request.form['slug']
        article.title = request.form['title']
        article.content = request.form['content']
        if 'preview' in request.form:
            flash('Remember this is just a preview: the article has not yet been saved.')
            return render_template('article_form.html', article=article, preview=True, action=url_for('edit_article', slug=slug))
        else:
            g.db.session.commit()
            flash('Article updated.')
            return redirect(url_for('article', slug=article.slug))
    else:
        return render_template('article_form.html', article=article, action=url_for('edit_article', slug=slug))

@app.route('/admin/drop/<path:slug>', methods=['GET', 'POST'])
@login_required
@only_admin
def drop_article(slug):
    article = models.Article.query.get(slug)
    if request.method == 'POST':
        if 'confirm' in request.form:
            g.db.session.delete(article)
            g.db.session.commit()
            flash("Article '%s' has been deleted." % article.title)
        return redirect(url_for('admin'))
    else:
        return render_template('confirm.html', action=url_for('drop_article', slug=slug),
                               query='delete the article titled "%s"' % article.title)

@app.route('/admin/sidebar', methods=['GET', 'POST'])
@login_required
@only_admin
def edit_sidebar():
    if request.method == 'POST' and 'action' in request.form:
        if request.form['action'] == 'new_link':
            link = models.SidebarLink(request.form['url'], request.form['label'], request.form['page'] if 'page' in request.form else None)
            cat = models.Sidebar.query.get(int(request.form['parent']))
            cat.links.append(link)
            g.db.session.add(link)
        elif request.form['action'] == 'edit_link':
            link = models.SidebarLink.query.get(request.form['id'])
            link.url = request.form['url']
            link.label = request.form['label']
            link.page = request.form['page'] if 'page' in request.form else None
        elif request.form['action'] == 'drop_link':
            link = models.SidebarLink.query.get(request.form['id'])
            g.db.session.delete(link)
        elif request.form['action'] == 'new_category':
            cat = models.Sidebar(request.form['name'])
            g.db.session.add(cat)
        elif request.form['action'] == 'edit_category':
            cat = models.Sidebar.query.get(request.form['id'])
            cat.name = request.form['name']
        elif request.form['action'] == 'drop_category':
            cat = models.Sidebar.query.get(request.form['id'])
            for link in cat.links:
                g.db.session.delete(link)
            g.db.session.delete(cat)
        g.db.session.commit()
        g.navbar = models.Sidebar.query.all()

    return render_template('edit_sidebar.html')

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        extra_headers = {}
        if 'return-addr' in request.form:
            extra_headers['Reply-To'] = request.form['return-addr'];
        with mail.record_messages() as outbox:
            msg = Message(recipients=[app.config['MAIL_DEFAULT_RECIPIENT']],
                          subject="Contact form message from %s" % (app.config['SERVER_NAME'] if app.config['SERVER_NAME'] is not None else 'the website'),
                          body=request.form['content'],
                          extra_headers=extra_headers)
            mail.send(msg)
            sent = outbox[0]
        flash("Message has been sent.")
        return redirect(url_for('article'))
    article = models.Article.query.get('contact')
    return render_template('contact_form.html', article=article)

@app.route('/download/<path:fname>')
def download(fname):
    recorder = models.DownloadHit.query.get(fname)
    if recorder is None:
        recorder = models.DownloadHit(fname)
        g.db.session.add(recorder)
    recorder.record()
    g.db.session.commit()
    # TODO: Redirect to configured static path of the download.
    return Response('Recorded hit on %s' % fname, mimetype='text/plain')

@app.route('/admin/forget/<path:fname>', methods=['GET', 'POST'])
@login_required
@only_admin
def forget_download(fname):
    hit = models.DownloadHit.query.get(fname)
    if hit is None:
        return redirect(url_for('admin'))
    elif request.method == 'POST':
        if 'confirm' in request.form:
            g.db.session.delete(hit)
            g.db.session.commit()
            flash('Download counter for %s reset (was: %d).' % (hit.path, hit.hit_count))
        return redirect(url_for('admin'))
    else:
        return render_template('confirm.html', action=url_for('forget_download', fname=fname),
                               query='forget the download count for "%s"' % fname)
