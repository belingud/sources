from flask import request, g
from flask_restful import abort

from FlaskWork.ext import cache
from Users.models import User


def login_required(fun):

    def wrapper(*args, **kwargs):
        token = request.form.get("token")

        if not token:
            abort(400, message="autn fail")

        user_id = cache.get(token)

        if not user_id:
            abort(400, message="token error")

        user = User.query.get(user_id)

        if not user:
            abort(401, message="user doesn't exist")
        g.user = user
        return fun(*args, **kwargs)
    return wrapper
