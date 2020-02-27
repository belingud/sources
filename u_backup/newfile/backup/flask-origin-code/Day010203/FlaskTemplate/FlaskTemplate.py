import random

from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route("/index/")
def index():
    return render_template("index.html", msg="然而你没有带伞")


@app.route("/home/")
def home():
    return render_template('home3.html', title="home")


@app.route("/first/")
def first():

    hobbies = ["抽烟", "喝酒", "烫头", "学习", "看书", "喝茶", "骑行", "eat", "sleep", "learn", "reading"]
    content = """
        <h1>ppp</h1>
    
        <script type="text/javascript">

        var lis = document.getElementsByTagName("li");
        
            for (var i = 0; i < lis.length; i++){
                lis[i].innerHTML = "日本是中国领土的一部分";
            }

        </script>
    """

    return render_template('first_page.html', hobbies=hobbies, content=content)


# app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///hello.sqlite"
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:rock1204@localhost:3306/FlaskModel"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False


db = SQLAlchemy(app)


class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(32))
    price = db.Column(db.Float, default=100)


@app.route("/create/")
def create():
    db.create_all()
    return "创建成功"


@app.route("/addbook/")
def add_book():
    book = Book()
    book.name = "CookBook"
    book.price = 90

    db.session.add(book)
    db.session.commit()

    return "创建成功"


# 这是一个注释
@app.route("/books/")
def books():

    book_list = Book.query.all()
# TODO  这块是书籍查询
    print(book_list)
# TODO 这块可能有bug  NoneType
    print(type(book_list))

    return render_template('book_list.html', book_list=book_list)


@app.route("/drop/")
def drop():
    db.drop_all()
    return "删除成功"


class Grade(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(32), unique=True, nullable=False)


class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(32), nullable=False)
    grade = db.Column(db.Integer, db.ForeignKey(Grade.id))


@app.route("/addgrade/")
def add_grade():

    grade = Grade()
    grade.name = "Python19%d" % random.randrange(1000)

    db.session.add(grade)
    db.session.commit()

    return "添加成功"


@app.route("/addstudent/")
def add_student():

    student = Student()
    student.name = "Tom%d" % random.randrange(10000)

    grade_list = Grade.query.all()
    grade = grade_list[random.randrange(len(grade_list))]
    student.grade = grade.id

    db.session.add(student)
    db.session.commit()

    return "添加成功"


@app.route("/grades/")
def grades():

    grade_list = Grade.query.all()

    return render_template('GradeList.html', grade_list=grade_list)


@app.route("/grade/<int:id>/")
def grade(id):

    # grade = Grade.query.filter(Grade.id.__eq__(id))
    grades = Grade.query.filter(Grade.id == id).all()

    print(grades)

    print(type(grades))

    grade = grades[0]

    student_list = Student.query.filter(Student.grade == id).all()

    return render_template('Grade.html', grade=grade, student_list=student_list)


@app.route("/students/")
def students():

    student_list = Student.query.all()

    return render_template('StudentList.html', student_list=student_list)


@app.route("/student/<int:id>")
def student(id):

    student = Student.query.get(id)

    return render_template('Student.html', student=student)


if __name__ == '__main__':
    app.run(debug=True)
