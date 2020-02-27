from FlaskProjectAdvanced.extension import db


class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    m_name = db.Column(db.String(256))
    m_detail = db.Column(db.String(256))