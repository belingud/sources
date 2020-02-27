from Blogs.route import blogs_api
from Learn.route import learn_api
from Users.route import users_api


def init_api(app):
    users_api.init_app(app)
    learn_api.init_app(app)
    blogs_api.init_app(app)
