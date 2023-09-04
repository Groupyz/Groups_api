from flask import jsonify, make_response
from DB.dbHandler import groupsHandler
from app import app
from DB.dbErrors import *
GROUP_PATH = "groups"


@app.route(f'/{GROUP_PATH}/<userId>', methods=['GET'])
def handleGet(userId):
    try:
        groups = groupsHandler.getAllGroupsDB(userId)
        groups_list = convert_db_item_to_list(groups)
        
        if groups != ERROR_GROUP_NOT_FOUND:
            return make_response(jsonify({'groups': groups_list}), 200)
        else:
            return make_response(jsonify({'error': ERROR_GROUP_NOT_FOUND}), 404)
    except Exception as e:
        error_message = DbErrors.handle_error(e)
        return make_response(jsonify({'error': error_message}), 500)


def convert_db_item_to_list(groups):
    groups_list = []
    for group in groups:
        groups_list.append({
            'user_id': group.user_id,
            'group_id': group.group_id,
            'group_name': group.group_name
        })
    return groups_list
    
