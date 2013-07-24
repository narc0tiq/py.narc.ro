from flask import g
from application import app, models
from datetime import datetime

@app.before_request
def start_timer():
    g.start_time = datetime.utcnow()
    g.datetime = datetime

@app.before_request
def setup_navigation():
    g.navbar = models.Sidebar.query.all()

@app.before_request
def init_db():
    g.db = models.db
