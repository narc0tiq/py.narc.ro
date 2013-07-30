import re
from datetime import datetime
from flask.ext.sqlalchemy import SQLAlchemy
from application.decorators import permalink

db = SQLAlchemy()

class Article(db.Model):
    slug = db.Column(db.String(200), primary_key=True)
    title = db.Column(db.String(200))
    content = db.Column(db.Text)

    def __init__(self, title, content, slug=None):
        self.title = title
        self.content = content
        self.slug = slug
        if not self.slug:
            self.slug = slugify(title)

    def __repr__(self):
        return '<Article %r>' % self.slug

    @permalink
    def permalink(self):
        return 'article', {'slug': self.slug}

slug_cleaner = re.compile('[^a-z0-9]+')
def slugify(text):
    clean_text = slug_cleaner.sub('-', text.lower()).strip('-')
    if not clean_text: # Empty slugs are bad!
        raise Exception("I don't like you.")
    return unicode(clean_text)


class User(db.Model):
    email = db.Column(db.String(200), primary_key=True)
    display_name = db.Column(db.String(50), nullable=True)

    def __init__(self, email, display_name=None):
        self.email = email
        self.display_name = display_name

    def __repr__(self):
        return '<User %r>' % self.email

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return self.email

def get_user_by_id(user_id):
    return User.query.get(user_id)

def get_user_from_browserid(response):
    if response['status'] != 'okay':
        return None

    candidate = get_user_by_id(response['email'])
    if candidate:
        return candidate

    new_user = User(response['email'])
    db.session.add(new_user)
    db.session.commit()
    return new_user


class Sidebar(db.Model):
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    name = db.Column(db.String(50), nullable=False)

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return '<Sidebar %r>' % self.name


class SidebarLink(db.Model):
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    url = db.Column(db.String(255))
    label = db.Column(db.String(50))
    page = db.Column(db.String(100), nullable=True)

    parent_id = db.Column(db.Integer, db.ForeignKey(Sidebar.id))
    parent = db.relationship(Sidebar, backref=db.backref('links', lazy='static'))

    def __init__(self, url, label, page=None):
        self.url = url
        self.label = label
        self.page = page

    def __repr__(self):
        return '<SidebarLink %r>' % self.label


class DownloadHit(db.Model):
    path = db.Column(db.String(255), primary_key=True)
    first_hit = db.Column(db.DateTime)
    last_hit = db.Column(db.DateTime)
    hit_count = db.Column(db.Integer)

    def __init__(self, path):
        self.path = path
        self.first_hit = datetime.now()
        self.last_hit = datetime.now()
        self.hit_count = 0

    def record(self):
        self.hit_count += 1
        self.last_hit = datetime.now()

    def __repr__(self):
        return '<DownloadHit %r, %r hits between %r - %r>' % (self.path, self.hit_count, self.first_hit, self.last_hit)


class Session(db.Model):
    uuid = db.Column(db.String(32), primary_key=True)
    data = db.Column(db.Binary)
    last_access = db.Column(db.DateTime)

    def __init__(self, uuid):
        self.uuid = uuid
        self.last_access = datetime.now()

    def __repr__(self):
        return '<Session %r>' % self.uuid


def bind(app):
    db.init_app(app)
    return db
