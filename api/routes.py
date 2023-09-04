import os
from flask import jsonify, make_response
import requests
from DB.dbHandler import groupsHandler
from app import app
from DB.dbErrors import *
from chatParser.chat_parser import JsonChatsToGroupConverter
GROUP_PATH = "groups"
BOT_URL = os.environ.get("BOT_URL")
BOT_URL_CHATS = BOT_URL + '/chats'


@app.route(f'/{GROUP_PATH}/<userId>', methods=['GET'])
def handleGet(userId):
    try:
        groups = groupsHandler.getAllGroupsDB(userId)
        if groups == ERROR_GROUP_NOT_FOUND:
            groups_json = requests.get(url=BOT_URL_CHATS)
            if groups_json is None:
                return make_response(jsonify({'error': ERROR_GROUP_NOT_FOUND}), 404)
            
            converter = JsonChatsToGroupConverter(userId)
            groups = converter.convert(groups_json)

        groups_list = convert_db_item_to_list(groups)
        return make_response(jsonify({'groups': groups_list}), 200)
 
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
    
