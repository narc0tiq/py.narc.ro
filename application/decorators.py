from functools import wraps
from flask import url_for
from werkzeug.routing import BuildError

def permalink(function):
    @wraps(function)
    def decorated(*args, **kwargs):
        endpoint, values = function(*args, **kwargs)
        try:
            return url_for(endpoint, **values)
        except BuildError:
            return
    return decorated
