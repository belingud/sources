from tornado.web import RequestHandler

from TornadoProject.ext import Base, engine


class UserHandler(RequestHandler):
    def get(self):
        self.write("user")


class DBHandler(RequestHandler):
    def get(self):
        action = self.get_query_argument("action")
        if action == "create":
            Base.metadata.create_all(engine)
        elif action == "drop":
            pass
        self.write("%s mission done" % action)


class UsersHandler(RequestHandler):
    def get(self):
        self.write("user")
