from flask import g
import rootpath

rootpath.append()
from backend.data_preparation.connection import Connection


def get_db():
    if 'db' not in g:
        g.db = Connection()()

    return g.db


def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()


def init_app(app):
    app.teardown_appcontext(close_db)
