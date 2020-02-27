from flask import Blueprint

blue = Blueprint("blue",__name__, url_prefix="/users")


@blue.route("/")
def index():
    return "Index Blue"


@blue.route("/home/")
def home():
    return "Home Blue"