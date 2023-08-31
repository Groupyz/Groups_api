import pytest
import json
import os
from app import db, app
from chatParser.parser_data_classes import Chat
from DB.models import Groups
from chatParser.filterer import GroupJsonFilterer
from chatParser.specification import GroupJsonSpecification
from chatParser.chat_parser import (
    JsonToGroupDCConverter,
    GroupDCToDBRecsConverter,
    JsonChatsToGroupConverter
    )



DUMMY_USER_ID = 123456789



@pytest.fixture(scope="session")
def chats_json():
    file_path = os.path.join(os.path.dirname(__file__), "groups_and_private.json")
    with open(file_path) as json_file:
        data = json.load(json_file)
    return data

@pytest.fixture(scope="session")
def only_group_chats_json():
    file_path = os.path.join(os.path.dirname(__file__), "dummy_group_chat.json")
    with open(file_path) as json_file:
        data = json.load(json_file)
    return data

@pytest.fixture(scope="session")
def private_json_chat():
    file_path = os.path.join(os.path.dirname(__file__), "dummy_private_chat.json")
    with open(file_path) as json_file:
        data = json.load(json_file)
    return data



def test_json_to_group_converter(chats_json):
    with app.app_context():
        converter = JsonChatsToGroupConverter(DUMMY_USER_ID)
        db_recs = converter.convert(chats_json)
        records_with_user_id = Groups.query.filter_by(user_id=DUMMY_USER_ID).all()

        delete_db_records_with_this_user_id(DUMMY_USER_ID)

        assert len(db_recs) == len(records_with_user_id)



def test_dc_to_db_recs_converter():
    dc_recs = create_multiple_chats(10)

    converter = GroupDCToDBRecsConverter()
    db_recs = converter.convert(dc_recs)

    assert len(db_recs) == len(dc_recs)
    if len(db_recs) > 0: assert db_recs[0].user_id == DUMMY_USER_ID


def test_json_to_data_class_converter(only_group_chats_json):
    converter = JsonToGroupDCConverter(DUMMY_USER_ID)
    dc_recs = converter.convert(only_group_chats_json)

    assert len(dc_recs) == len(only_group_chats_json)
    if len(dc_recs) > 0: assert dc_recs[0].user_id == DUMMY_USER_ID


def test_group_chat_filterer(chats_json):
    filterer = GroupJsonFilterer()
    filtered_json = filterer.filter(chats_json)

    assert len(filtered_json) == 2


def test_group_specification(private_json_chat, only_group_chats_json):
    specifictaion = GroupJsonSpecification()

    assert False == specifictaion.is_satisfied(private_json_chat[0])
    assert True == specifictaion.is_satisfied(only_group_chats_json[0])


def test_create_chat_data_class():
    group_id, gorup_name, user_id = "123456789", "test_group", DUMMY_USER_ID
    chat = create_dummy_chat_data_class(
        group_id=group_id, group_name=gorup_name, user_id=user_id
    )
    assert chat.group_id == group_id
    assert chat.group_name == gorup_name
    assert chat.user_id == user_id



def create_multiple_chats(num_records):
    chats = []
    for i in range(num_records):
        group_id = str(i + 1)  # Generating a unique group ID
        group_name = f"group_{i + 1}"  # Generating a unique group name
        chat = create_dummy_chat_data_class(group_id=group_id, group_name=group_name)
        chats.append(chat)

    return chats


def create_dummy_chat_data_class(**kwargs):
    default = {
        "group_id": "123456789",
        "group_name": "test_group",
        "user_id": DUMMY_USER_ID,
    }
    default.update(kwargs)
    chat = Chat(**default)

    return chat


def delete_db_records_with_this_user_id(user_id: str):
    records_with_user_id = Groups.query.filter_by(user_id=user_id).all()
    for record in records_with_user_id:
        db.session.delete(record)
    db.session.commit()