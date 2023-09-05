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


@app.route(f'/{GROUP_PATH}/<userId>', methods=['GET'] )
def handleGet(userId):
    try:
        return create_grps_response(userId)
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

def create_grps_response(user_id: int) -> requests.Response:
    response = None

    # try to find recs in db
    groups = groupsHandler.getAllGroupsDB(user_id)

    # if no recs in db --> get from recs from bot_api
    if groups == ERROR_GROUP_NOT_FOUND:
        groups = get_grps_from_bot(user_id)

    groups_list = convert_db_item_to_list(groups)
    response = make_response(jsonify({'groups': groups_list}), 200)

    return response

def get_grps_from_bot(user_id :int) -> list:

    bot_res = requests.get(url=BOT_URL_CHATS)
    groups_json = bot_res.json()

    if groups_json is None:
        raise Exception(ERROR_GROUP_NOT_FOUND)

    converter = JsonChatsToGroupConverter(user_id)
    groups = converter.convert(groups_json)

    return groups