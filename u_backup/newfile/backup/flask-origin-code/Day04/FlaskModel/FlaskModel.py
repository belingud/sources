import random
from operator import or_, and_

from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///flaskmodel.sqlite"


db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(32), unique=True)
    password = db.Column(db.String(256))

    def save(self):
        db.session.add(self)
        db.session.commit()

    def check_password(self, password):
        return self.password == password


@app.route("/init/")
def init():
    db.create_all()
    return "初始化成功"


@app.route('/login/', methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template('login.html')
    elif request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        # 根据用户名查询用户
        users = User.query.filter(User.name.__eq__(username)).all()

        # 判定用户是否存在
        if not users:
            return "用户不存在"

        # 获取我们第一个用户
        user = users[0]

        # 验证密码
        if not user.check_password(password):
            return "密码错误"

        # 重定向到个人中心
        response = redirect(url_for("mine"))
        # 记录会话状态
        response.set_cookie("username", username)
        return response


@app.route("/mine/")
def mine():

    username = request.cookies.get("username")

    if username:

        return render_template('mine.html', username=username)
    else:
        return redirect(url_for("login"))


@app.route('/register/', methods=["GET", "POST"])
def register():
    # 根据不同的请求方法 做不同的处理
    if request.method == "GET":

        return render_template('register.html')

    elif request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        user = User(name=username, password=password)

        user.save()
        return redirect(url_for("login"))


class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(32), unique=True)
    score = db.Column(db.Integer, default=60)

    def save(self):
        db.session.add(self)
        db.session.commit()


@app.route("/addstudent/")
def add_student():

    student = Student(name="小明%d" % random.randrange(10000), score=random.randrange(100))
    student.save()

    return "添加成功"


@app.route("/students/")
def students():

    # student_list = Student.query.filter(Student.score > 80).all()
    # student_list = Student.query.filter(Student.score > 60).filter(Student.score < 80).all()
    # student_list = Student.query.filter(Student.score.__lt__(60)).all()
    # student_list = Student.query.filter(Student.score.in_([60, 81, 100, 200])).all()

    # 通常级联查询   条件是确切的  = 那种     条件 改成  属性=值
    # student_list = Student.query.filter_by(score = 80).all()

    # student_list = Student.query.offset(3).limit(3).all()
    # student_list = Student.query.order_by(text("-score")).all()

    # order_by必须放在最前面   limit 和 offset无顺序   实际上都是先  offset再limit

    # student_list = Student.query.order_by("score").limit(4).offset(3).all()

    # BaseQuery是可迭代元素   all只是将格式转换为了 列表
    # student_list = Student.query.order_by("score")
    # student = Student.query.first()
    #
    # print(student)
    #
    # print(type(student))

    # return render_template("student_list.html", student_list=student_list)

    # 可以从客户端接受参数  参数是页码  每一个三条数据
    # page = request.args.get("page", 1, type=int)
    #
    # student_list = Student.query.offset(3*(page-1)).limit(3).all()
    #
    # return render_template("student_list.html", student_list=student_list)

    pagination = Student.query.paginate()

    return render_template("student_list.html", pagination=pagination)


@app.route("/students2/")
def students2():

    student_list = Student.query.filter(and_(Student.score.__gt__(60), Student.score.__lt__(90)))

    return render_template("student_list2.html", student_list=student_list)


@app.route("/dropfirst/")
def drop_first():
    student = Student.query.order_by(text("-score")).first()

    print(student.score)

    db.session.delete(student)
    db.session.commit()

    return "88"


@app.route("/updatescore/")
def update_score():
    student = Student.query.order_by(text("score")).first()

    print(student.score, student.id)

    student.score = 100

    db.session.add(student)
    db.session.commit()

    return "完成"


if __name__ == '__main__':
    app.run(debug=True)
