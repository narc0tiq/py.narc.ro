from __future__ import unicode_literals, absolute_import
from collections import OrderedDict, namedtuple

from flask import request, session, g, redirect, url_for, abort, \
        render_template, flash

from application import app

NavbarItem = namedtuple('NavbarItem', ['page_name', 'url', 'title'])
LocalNav = lambda page, title: NavbarItem(page, url_for(page), title)
RemoteNav = lambda url, title: NavbarItem(None, url, title)

@app.before_request
def setup_navigation():
    g.navbar = [
        ('Navigation', [LocalNav('index', "Index"),
                        LocalNav('admin', "Admin")]),
        ('Related Sites', [RemoteNav('http://wiki.narc.ro/', "NarcWiki")])]

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/admin/')
def admin():
    g.active_page = 'admin'
    return render_template('index.html')

