from flask import Blueprint, render_template, g, request, make_response

from FlaskProjectAdvanced.extension import cache
from .models import User


user_blue = Blueprint("user_blue", __name__, url_prefix="/users")


@user_blue.route("/")
def index():
    return "Hello Index"


@user_blue.route("/create/")
def create():

    g.msg = "小伙子睡着了"
    print("create", g.data)

    return render_template('index.html')


# @user_blue.before_request
# def before():
#
#     print("before")
#
#     g.data = "给你"

@user_blue.route("/register/")
def register():
    return render_template("register.html")


@user_blue.route("/login/", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        if cache.get("username"):
            return render_template("usercenter.html", username=cache.get("username"))
        else:
            return render_template("login.html")
    elif request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        # name = cache.get(username)
        user = User.query.filter(User.name == username).all()[0]
        if not user:
            return "username not exist"
        elif not user.check_passwd(password=password):
            return "wrong password"
        else:
            cache.set("username", username)
            return render_template("usercenter.html", username=username)


@user_blue.route("/register/", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")
    elif request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        name = cache.get(username)
        if name:
            return render_template("usercenter.html", username=username)
        else:
            user = User.query.filter(User.name == username).all()[0]
            sqlname = user.name
            if sqlname:
                return "username already exist"
            else:
                user = User(name=username, password=password)
                user.save()

                return render_template("login.html")






