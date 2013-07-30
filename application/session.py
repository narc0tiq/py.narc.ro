from uuid import uuid4, UUID
from datetime import datetime, timedelta
import pickle

from werkzeug.datastructures import CallbackDict
from flask.sessions import SessionInterface, SessionMixin
from application.models import db, Session

class SessionData(CallbackDict, SessionMixin):
    def __init__(self, initial=None, sid=None, new=False):
        def on_update(self):
            self.modified = True
        CallbackDict.__init__(self, initial, on_update)
        self.sid = sid
        self.new = new
        self.modified = False

class SQLSession(SessionInterface):
    def open_session(self, app, request):
        sid = request.cookies.get(app.session_cookie_name)
        if not sid:
            # No existing session, so create one
            return SessionData(sid=str(uuid4()), new=True)

        sess = Session.query.get(sid)
        if not sess:
            # No session in the database; return a fresh one
            return SessionData(sid=str(uuid4()), new=True)

        data = pickle.loads(sess.data)
        return SessionData(sid=sid, initial=data)

    def save_session(self, app, sdata, response):
        cookie_domain = self.get_cookie_domain(app)
        sess = Session.query.get(sdata.sid)

        if not sdata:
            # Session has become empty (i.e. `if not some_dict`), so drop it
            if sess:
                db.session.delete(sess)
        else:
            if not sess:
                sess = Session(sdata.sid)
                db.session.add(sess)
            sess.data = pickle.dumps(dict(sdata), protocol=2)
            sess.last_access = datetime.now()

        # Expire old(er than 30 days) sessions
        Session.query.filter(Session.last_access < (datetime.now() - timedelta(days=30))).delete()
        db.session.commit()

        response.set_cookie(app.session_cookie_name, sess.uuid,
                            expires=(datetime.now() + timedelta(days=30)),
                            domain=cookie_domain, httponly=True)
