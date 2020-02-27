from flask_restful import Api

from Users.views import UsersResource

users_api = Api(prefix='/users')


users_api.add_resource(UsersResource, "/")
