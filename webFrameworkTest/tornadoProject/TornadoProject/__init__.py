import os

from tornado.web import Application
from App.views import IndexHandler
from TornadoProject.routers import urlpatterns
from TornadoProject.settings import BASE_DIR, DEBUG
from Users.views import UserHandler


def create_app():
    # app = Application(handlers=[UserHandler, IndexHandler],)
    app = Application(handlers=urlpatterns, template_path=os.path.join(BASE_DIR, 'templates'),
                      static_path=os.path.join(BASE_DIR, 'static'), debug=DEBUG)

    return app
