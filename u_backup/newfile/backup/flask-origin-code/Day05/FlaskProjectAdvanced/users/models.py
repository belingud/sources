from FlaskProjectAdvanced.extension import db


class User(db.Model):

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(32), unique=True)
    password = db.Column(db.String(256))

    # package the codes into a class method for convenience
    def save(self):
        db.session.add(self)
        db.session.commit()

    def check_passwd(self, password):
        return self.password == password
