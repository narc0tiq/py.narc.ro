from __future__ import unicode_literals, absolute_import
from flask import Flask
from application import config, models

app = Flask(__name__)
app.config.from_object(config)
app.config.from_envvar('NARCRO_CONFIG', silent=True)

models.bind(app)

import application.hooks
import application.routes
