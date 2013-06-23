from __future__ import unicode_literals, absolute_import
from flask import Flask
from flask.ext.login import LoginManager
from flask.ext.browserid import BrowserID
from flask.ext.misaka import Misaka
from application import config, models

app = Flask(__name__)
app.config.from_object(config)
app.config.from_envvar('NARCRO_CONFIG', silent=True)

models.bind(app)
db = models.db

login_manager = LoginManager()
login_manager.user_loader(models.get_user_by_id)
login_manager.init_app(app)

browser_id = BrowserID()
browser_id.user_loader(models.get_user_from_browserid)
browser_id.init_app(app)

Misaka(app, fenced_code=True, html=True, strikethrough=True, superscript=True,
       tables=True, toc=True, xhtml=False, intra_emphasis=False)

import application.hooks
import application.routes
