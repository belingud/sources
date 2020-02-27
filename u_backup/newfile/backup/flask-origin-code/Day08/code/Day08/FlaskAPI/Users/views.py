import uuid

from flask import request
from flask_restful import Resource, abort, reqparse

from FlaskWork.ext import cache
from Users.models import User

# 先声明请求转换器
parse = reqparse.RequestParser()

# 添加请求参数规则
parse.add_argument("username", required=True, type=str, help="username can't be blank")
parse.add_argument("password", required=True, type=str, help="password can't be blank")
parse.add_argument("action", required=True, type=str, help="please supply action")


class UsersResource(Resource):

    def post(self):
        # 转换参数    根据规则去过滤
        args = parse.parse_args()
        # form 获取html中form表单中的数据，如果客户端不是html  也同样可以提交表单数据
        action =args.get("action")

        if action == "register":
            return self.do_register()
        elif action == "login":
            return self.do_login()

    def do_register(self):
        args = parse.parse_args()
        username = args.get("username")
        password = args.get("password")

        # if not username:
        #     # return {"msg": "username can't be blank"}
        #     abort(400, message="username can't be blank")

        user = User(username=username, password=password)

        if not user.save():
            data = {
                "msg": "register fail",
                "status": 400
            }

            return data

        data = {
            "msg": "register success",
            "status": 201
        }

        return data

    def do_login(self):

        username = request.form.get("username")
        password = request.form.get("password")

        users = User.query.filter(User.username.__eq__(username)).all()

        if not users:

            data = {
                "msg": "user doesn't exist",
                "status": 401
            }

            return data

        user = users[0]

        if not user.check_password(password):

            data = {
                "msg": "password error",
                "status": 401
            }

            return data
        # 生成令牌    唯一
        token = uuid.uuid4().hex

        # 服务器记录令牌
        cache.set(token, user.id, timeout=60*60*24*7)

        # 令牌返回给客户端
        data = {
            "msg": "login sucess",
            "status": 200,
            "data": {
                "token": token
            }
        }

        return data