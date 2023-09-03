from app import db
ERROR_GROUP_NOT_FOUND = 'Groups not found'


class DbErrors():
    def handle_error(error):
        db.session.rollback()
        error_message = str(error)
        return error_message