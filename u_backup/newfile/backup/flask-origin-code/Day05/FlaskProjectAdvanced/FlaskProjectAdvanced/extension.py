from flask_caching import Cache
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()
migrate = Migrate()
cache = Cache(config={
    "CACHE_TYPE": "redis",
    "CACHE_REDIS_URL": "redis://:000000@127.0.0.1:6379/1",
})


def init_ext(app):
    db.init_app(app)
    migrate.init_app(app, db)
    cache.init_app(app)

