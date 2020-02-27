from flask import Blueprint

from App.extension import db

from App.models import User


user_blue = Blueprint("user_blue", __name__, url_prefix="/users")


@user_blue.route("/")
def index():
    return "Hello Index"


@user_blue.route("/create/")
def create():
    db.create_all()
    return "创建成功"