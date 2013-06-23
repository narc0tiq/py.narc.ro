# Default config for the narc.ro application.
# Override by pointing at a file using env("NARCRO_CONFIG")

SQLALCHEMY_DATABASE_URI = 'sqlite:///.narc.ro.sqlite3.db'
SQLALCHEMY_ECHO = True

SERVER_NAME = 'flask.narc.ro'
DEBUG = True
DEBUG_INTERACTIVE = False
SECRET_KEY = 'Developer Secret (not so secret)'

# The webmaster is the only person allowed to add/edit articles.
# Note that anyone can view the admin area, though (by design)
WEBMASTER_EMAIL = 'webmaster@narc.ro'
