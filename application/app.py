from __future__ import unicode_literals, absolute_import
from flask import Flask, request, session, g, redirect, url_for, abort, \
        render_template, flash

from application import config

app = Flask('application')
app.config.from_object(config)
app.config.from_envvar('NARCRO_CONFIG', silent=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/admin/')
def admin():
    g.active_page = 'admin'
    return render_template('index.html')

