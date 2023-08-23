import pytest
import json
import os
from flask_sqlalchemy import SQLAlchemy
from app import db, app
from chat_parser.chat_parser import ChatParser, CHAT_ERROR_PARSING
from chat_parser.parser_data_classes import Summary, Chat
from DB.models import Groups

# TODO: make dynamic
INVALID_JSON = "invalid json"
DUMMY_USER_ID = "123456789"


@pytest.fixture(scope="session")
def chats_json():
    file_path = os.path.join(os.path.dirname(__file__), "dummy_chats.json")
    with open(file_path) as json_file:
        data = json.load(json_file)
    return data


@pytest.fixture(scope="session")
def chats_parser(chats_json):
    parser = ChatParser(chats_json, DUMMY_USER_ID)
    return parser


@pytest.fixture(scope="session")
def json_chat():
    file_path = os.path.join(os.path.dirname(__file__), "dummy_chat.json")
    with open(file_path) as json_file:
        data = json.load(json_file)
    return data


# Tests that file is retrived & valid
def test_json_data(chats_json):
    assert isinstance(chats_json, list)
    assert len(chats_json) > 0


# Test json creates succesuf parse with apropriate records
def test_positive_parser_flow(chats_parser):
    summary = chats_parser.parse()

    assert summary.total_records_created == len(chats_json)
    records_with_user_id = Groups.query.filter_by(user_id=DUMMY_USER_ID).all()
    assert len(records_with_user_id) == len(chats_json)


# Test bad json shows logical error
def test_negative_parser_flow(chats_json):
    invalid_json = make_json_invalid(chats_json)
    try:
        parser = ChatParser(invalid_json, DUMMY_USER_ID)
        parser.parse()
    except Exception as e:
        assert e == INVALID_JSON


# check that for each json obj an data class 'chats' instance is create with valid data
def test_chat_data_class_creation(chats_parser, chats_json):
    chats = chats_parser.create_chats()
    assert len(chats) == len(chats_json)
    assert chats[0].user_id == DUMMY_USER_ID


# recive json chat obj return chat obj with valid user id
def test_succseful_create_chat_from_chat_json(json_chat, chats_parser):
    with app.app_context():
        chat = chats_parser.create_chat(json_chat)
        assert chat.user_id == DUMMY_USER_ID
        assert chat.group_id == json_chat.get("id").get("_serialized")
        assert chat.group_name == json_chat.get("name")

        delete_db_records_with_this_user_id(DUMMY_USER_ID)


# invalid chat json
def test_failed_create_chat_from_chat_json(json_chat, chats_parser):
    try:
        json_chat.pop("name")
        chats_parser.create_chat(json_chat)
    except KeyError as e:
        assert str(e) == CHAT_ERROR_PARSING


# Test creates DB records from chats data class
def test_create_db_record_from_chat_class(chats_parser):
    with app.app_context():
        chats = create_multiple_chats(num_records=10)
        chats_parser.create_db_records(chats)
        records_with_user_id = Groups.query.filter_by(user_id=DUMMY_USER_ID).all()
        assert len(records_with_user_id) == len(chats)

        delete_db_records_with_this_user_id(DUMMY_USER_ID)


def test_create_chat_data_class():
    group_id, gorup_name, user_id = "123456789", "test_group", DUMMY_USER_ID
    chat = create_dummy_chat_data_class(
        group_id=group_id, group_name=gorup_name, user_id=user_id
    )
    assert chat.group_id == group_id
    assert chat.group_name == gorup_name
    assert chat.user_id == user_id


def test_parser_summary():
    len_data_variables, len_json = 10, 10
    summary = Summary(len_data_variables, len_json, DUMMY_USER_ID)
    assert summary.total_records_created == len_data_variables
    assert summary.total_records_failed == 0
    assert summary.user_id == DUMMY_USER_ID


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
