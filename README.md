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


## Running the code ##

If you have python, flask and sqlalchemy installed and available (virtualenv is
recommended, but not required), it should be as simple as running `python -m
application`.

Note that, on the narc.ro website, there is a front-end Apache server that
(currently) is configured to proxy requests to the resulting python-powered
HTTP server. Other deployment options exist, and you are fully encouraged to
look into them, as I will be.
