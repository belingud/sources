from Movies.views import movies_blue
from Users.views import users_blue


def init_blue(app):
    app.register_blueprint(blueprint=users_blue)
    app.register_blueprint(blueprint=movies_blue)
