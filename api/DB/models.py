from app import db


class Groups(db.Model):
    __tablename__ = "groups"

    user_id = db.Column(db.Integer, primary_key=True)
    group_id = db.Column(db.Integer, nullable=False)
    group_name = db.Column(db.String(80), nullable=False)
