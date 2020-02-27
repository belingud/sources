from datetime import timedelta

from flask import Flask, render_template, request, Response, make_response, redirect, url_for, abort, session

app = Flask(__name__)
app.config["SECRET_KEY"] = "123"


@app.route('/', methods=["GET", "POST", "PUT", "DELETE"])
def hello_world():

    print(request.method)

    if request.method == "GET":

        print(request.remote_addr)

        print(request.args)

        print(request.args.get("username"))

        print(request.args.get("hobby"))

        print(request.args.getlist("hobby"))

        return render_template('index.html')
    elif request.method == "POST":
        return "听说你是POST"
    elif request.method == "PUT":
        return "PUT没听过"


@app.route("/register/")
def register():
    return render_template('register.html')


@app.route("/doregister/", methods=["GET", "POST"])
def do_register():

    print(request.form)

    username = request.form.get("username")

    password = request.form.get("password")

    print(username, password)

    # 数据存储

    return "注册成功"


@app.route("/login/")
def login():
    return render_template('login.html')


@app.route("/dologin/", methods=["POST"])
def do_login():
    print(request.form)

    username = request.form.get("username")

    password = request.form.get("password")

    print(username, password)

    # 数据读取， 数据校验

    # response = Response("login success")

    # response = make_response("login fail", 400)
    # return response

    if username == "Rock" and password == "110":
        response = Response("登录成功")
        # response.set_cookie("username", "Rock", max_age=60)
        # 存cookie
        # response.set_cookie("username", "Rock")
        session["username"] = "Rock"
        # 持久化
        session.permanent = True
        session.permanent_session_lifetime = timedelta(days=7)
    else:
        response = Response("用户名或密码错误")
    return response


@app.route("/users/")
def users():
    # return redirect("/")
    # return redirect(url_for('do_register'))

    # abort(400)

    # cookie实现
    # username = request.cookies.get("username")
    # session实现
    username = session.get("username")

    print(username)

    if username:
        return "欢迎回来%s <a href='/logout/'>退出</a>" % username

    # 未登录就要跳转登录页面
    return redirect(url_for("login"))


@app.route("/logout/")
def logout():
    response = Response("退出成功")

    # response.delete_cookie("username")

    # response.delete_cookie("session")
    # session.pop("username")
    # del session["username"]
    session["username"] = None

    return response


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")
