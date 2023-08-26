from app import db
from sqlalchemy.orm import validates
class Groups(db.Model):
    __tablename__ = "groups"

    user_id = db.Column(db.Integer, primary_key=True)
    group_id = db.Column(db.String(80), nullable=False, primary_key=True)
    group_name = db.Column(db.String(80), nullable=False)

    @validates("group_id")
    def validate_group_id(self, key, value):
        if not isinstance(value, str):
            raise ValueError("group_id must be a string")
        return value


