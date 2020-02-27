from FlaskWork.ext import db


class Book(db.Model):

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    b_name = db.Column(db.String(32))
    b_price = db.Column(db.Float, default=100)

    def save(self):
        try:
            db.session.add(self)
            db.session.commit()
        except Exception as e:
            print(e)
            return False
        return True

    def to_dict(self):
        return {"id": self.id, "b_name": self.b_name, "b_price": self.b_price}
