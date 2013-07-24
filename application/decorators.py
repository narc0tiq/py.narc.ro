from functools import wraps
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

def only_admin(function):
    @wraps(function)
    def decorated(*args, **kwargs):
        if current_user.email != app.config['WEBMASTER_EMAIL']:
            abort(403)
        return function(*args, **kwargs)
    return decorated
