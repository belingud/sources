from flask import Flask

from App.extension import init_ext
from App.settings import envs
from App.views import init_blue


def create_app(env):
    # 创建Flask对象
    app = Flask(__name__)

    # 加载配置  初始化配置
    app.config.from_object(envs.get(env))

    # 初始化扩展库  加载扩展库
    init_ext(app)

    # 初始化路由  加载路由
    init_blue(app)

    return app