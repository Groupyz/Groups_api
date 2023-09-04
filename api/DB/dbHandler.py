from DB.models import Groups
from sqlalchemy import func
from app import db
from DB.dbErrors import *

class groupsHandler():
    def getAllGroupsDB(user_id):
        allGroups = Groups.query.filter_by(user_id=user_id).all()
        if allGroups:
            return allGroups
        else:
            return ERROR_GROUP_NOT_FOUND
        
def generate_id():
    max_id = db.session.query(func.max(Groups.user_id)).scalar()
    res = (max_id or 0) + 1
    return res
