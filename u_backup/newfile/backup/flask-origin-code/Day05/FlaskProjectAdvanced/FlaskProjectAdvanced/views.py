import random

from flask import request

from movies.views import movie_blue
from users.views import user_blue


def init_blue(app):
    app.register_blueprint(blueprint=user_blue)
    app.register_blueprint(blueprint=movie_blue)

