from flask import Blueprint

blue2 = Blueprint("blue2", __name__, url_prefix="/orders")


@blue2.route("/")
def haha():
    return "haha blue2"


@blue2.route("/ppp/")
def ppp():
    return "ppp"