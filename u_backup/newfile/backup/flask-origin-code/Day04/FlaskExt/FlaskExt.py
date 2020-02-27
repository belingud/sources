from flask import Flask
from flask_script import Manager
from flask_sqlalchemy import SQLAlchemy

from users_view import blue
from orders_view import blue2

app = Flask(__name__, static_folder='haha/ddd')


app.register_blueprint(blueprint=blue)
app.register_blueprint(blueprint=blue2)


manager = Manager(app=app)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///test.sqlite"

db = SQLAlchemy(app)



class Student(db.Model):

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(32), unique=True)


if __name__ == '__main__':
    manager.run()
