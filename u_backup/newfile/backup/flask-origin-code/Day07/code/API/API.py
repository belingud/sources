from flask import Flask, jsonify
from flask_restful import Api, Resource

app = Flask(__name__)

# api = Api(app)
#
#
# class Hello(Resource):
#
#     def get(self):
#         return {"hello": "world"}
#
#     def post(self):
#         return {"msg": "POST OK"}
#
#     def put(self):
#         return {"hehe": "hehe What"}
#
#     def delete(self):
#         return {"hehe": "Delete What"}
#
#
# # ① 代表资源     ② 代表路由
# api.add_resource(Hello, "/ooo/")

# @app.route("/")
def index():
    return "Index"


app.add_url_rule("/hehe/", "index", index)


if __name__ == '__main__':
    app.run()
