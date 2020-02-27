from FlaskWork.ext import db
from Users.models import User


class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(32), nullable=False)
    content = db.Column(db.String(256), nullable=False)
    b_owner = db.Column(db.Integer, db.ForeignKey(User.id))

    def save(self):
        try:
            db.session.add(self)
            db.session.commit()
        except Exception as e:
            print(e)
            return False
        return True
