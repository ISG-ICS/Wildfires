import psycopg2.pool
import rootpath
from flask import g

rootpath.append()
from paths import DATABASE_CONFIG_PATH
from utilities.ini_parser import parse


def get_db():
    if 'pool' not in g:
        g.pool = psycopg2.pool.ThreadedConnectionPool(1, 5, **parse(DATABASE_CONFIG_PATH, 'postgresql'))
    return g.pool


def close_db(e=None):
    pool = g.pop('pool', None)
    if pool is not None:
        pool.closeall()


def init_app(app):
    app.teardown_appcontext(close_db)
