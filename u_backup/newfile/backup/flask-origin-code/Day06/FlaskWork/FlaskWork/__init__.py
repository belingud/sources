from flask import Flask

from FlaskWork.ext import init_ext
from FlaskWork.settings import envs
from FlaskWork.views import init_blue


def create_app(env):
    # 创建App
    app = Flask(__name__, static_folder="../static", template_folder="../templates")

    # 加载配置
    app.config.from_object(envs.get(env))

    # 加载第三方库
    init_ext(app)

    # 初始化路由
    init_blue(app)
    return app
