from flask import Flask

from FlaskProjectAdvanced.extension import init_ext
from FlaskProjectAdvanced.middleware import load_middleware
from FlaskProjectAdvanced.settings import envs
from FlaskProjectAdvanced.views import init_blue


def create_app(env):
    # 创建Flask对象
    app = Flask(__name__, template_folder='../templates')

    # 加载配置  初始化配置
    app.config.from_object(envs.get(env))

    # 初始化扩展库  加载扩展库
    init_ext(app)

    # 加载中间件
    load_middleware(app)

    # 初始化路由  加载路由
    init_blue(app)

    return app