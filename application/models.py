import re
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

def bind(app):
    db.init_app(app)
    return db
