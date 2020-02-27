from Book.route import books_api


def init_api(app):
    books_api.init_app(app)
