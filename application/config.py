# Default config for the narc.ro application.
# Override by pointing at a file using env("NARCRO_CONFIG")

SQLALCHEMY_DATABASE_URI = 'sqlite:///.narc.ro.sqlite3.db'
SQLALCHEMY_ECHO = True

SERVER_NAME = 'flask.narc.ro'
DEBUG = True
DEBUG_INTERACTIVE = False
SECRET_KEY = 'Developer Secret (not so secret)'
