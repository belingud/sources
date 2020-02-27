from App.views.movie_view import movie_blue
from App.views.user_view import user_blue


def init_blue(app):
    app.register_blueprint(blueprint=user_blue)
    app.register_blueprint(blueprint=movie_blue)