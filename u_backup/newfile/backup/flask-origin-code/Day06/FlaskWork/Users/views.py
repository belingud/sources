from flask import Blueprint, render_template, request, redirect, url_for, session
from .models import User

users_blue = Blueprint("users_blue", __name__, url_prefix="/users")


@users_blue.route("/register/", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")
    elif request.method == "POST":

        username = request.form.get("username")
        password = request.form.get("password")

        email = request.form.get("email")
        icon = request.files.get("icon")

        print(username, password, email, icon)

        path = None

        if icon:
            try:
                ext = "." + icon.filename.split(".")[-1]
            except Exception as e:
                ext = ".jpg"

            # path 应该是icon进行了存储操作产生的地址
            path = "/static/icons/" + username + ext
            save_path = "/home/vic/PycharmProjects/flask-class-code/Day06/FlaskWork/static/icons/" + username + ext

            icon.save(save_path)

        user = User(name=username, password=password, email=email, icon=path)

        if user.save():

            return redirect(url_for("users_blue.login"))
        else:
            return "注册失败"


@users_blue.route("/login/", methods=["GET","POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    elif request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        users = User.query.filter(User.name.__eq__(username)).all()

        if not users:
            return "用户不存在"

        user = users[0]

        if not user.check_password(password):
            return "密码错误"

        session["username"] = user.name
        session["icon"] = user.icon

        return redirect(url_for("movies_blue.home"))

