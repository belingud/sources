import random

from flask import request


def load_middleware(app):

    @app.before_request
    def app_before():
        print(request.remote_addr)
        print(request.url)
        print(request.path)

        if request.path == "/movies/":
            addr = request.remote_addr
            ip = addr.split(".")[-1]
            if int(ip) > 50:
                if random.randrange(100) > 20:
                    return "恭喜您特等奖"

    @app.before_request
    def before():
        print("before")

    @app.after_request
    def after(resp):
        print(type(resp))
        print("xxx")

        return resp

    @app.errorhandler(500)
    def error500(exce):

        print(type(exce))

        return "跳转到首页"
