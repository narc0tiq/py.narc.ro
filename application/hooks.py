from flask import g
from application import app, models

@app.before_request
def init_db():
    g.db = models.db
