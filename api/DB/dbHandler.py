from DB.models import Groups
from sqlalchemy import func
from app import db


def generate_id():
    max_id = db.session.query(func.max(Groups.user_id)).scalar()
    res = (max_id or 0) + 1
    return res
