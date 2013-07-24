This is the new variant of the [narc.ro](http://narc.ro/) website. It is written
in [Python](http://python.org/), using [Flask](http://flask.pocoo.org/) and
[SQLAlchemy](http://sqlalchemy.org/).

As with the previous version (which was written in PHP with PDO/SQLite), it is
intended to be as small as possible, with an emphasis on code readability at the
cost of flexibility (if the trade-off is necessary).

It is also somewhat of a Flask learner's project -- there are almost certainly
going to be things I will do that would be easier using more advanced techniques
and I may upgrade to those advanced techniques as I tinker with it. You are
advised to be aware of this fact if you intend to reuse the code.


## License ##

You are fully encouraged to consider this work Public Domain, or otherwise under
the least strict licensing terms available in your legal area. Do what you want
with it, I'm just writing the thing.


## Dependencies ##

**py.narc.ro** requires a working Python environment with the following pypy
packages installed:

 * flask
 * flask-misaka
 * flask-sqlalchemy
 * flask-browserid

Note that flask-browserid has been modified to use Flask's normal URL
generation mechanism (url_for) to create URLs in its internal template, which
itself has changed to be exposed as a regular template. These changes are
available [on Github](https://github.com/narc0tiq/flask-browserid/tree/use-url_for),
but will probably not be pull-requested to the upstream extension until the
template generation can be made more efficient (and that's *not* one of my
priorities).

Given that, setting up the environment for py.narc.ro should be as simple as:

```
[user@host ~]$ git clone https://github.com/narc0tiq/flask-browserid.git --branch use-url_for
[user@host ~]$ sudo pip install flask flask-misaka flask-sqlalchemy git+file://flask-browserid/
```

Messing around with [virtualenv](http://www.virtualenv.org/) is left as an
exercise to the reader, but rest assured it has been tested and  works just
fine.


## Installing ##

Before you can do much with a fresh new copy of py.narc.ro, you need to have it
create its database. The simplest way to do this is, while in the py.narc.ro
directory:

```
$ python
>>> from application import app, db
>>> with app.test_request_context():
...   db.create_all()
...
>>> exit()
```

This should create all of the tables and allow the application to run
successfully (albeit with no content whatsoever). From here, you'll probably
want to add a `config.py` with your email set as the webmaster address:

```
$ echo "WEBMASTER_EMAIL = 'you@example.org'" >> config.py
```

You may also want to look at the interesting settings in `application/config.py`,
and override anything you don't particularly like (don't edit the default
config, add overridden values to `config.py` instead). As an example, here's
what I'm using on one of my dev environments:

```
(venv)[narc@somewhere ~/src/py.narc.ro]% cat config.py
DEBUG_INTERACTIVE = True
LISTEN_INTERFACE = '0.0.0.0'
```


## Running the code ##

If you have python, flask and sqlalchemy installed and available (virtualenv is
recommended, but not required), it should be as simple as running `python -m
application`.

Note that, on the narc.ro website, the code is currently being run by Apache2
with mod_wsgi. A .wsgi file is included as a demonstration of a working setup.
