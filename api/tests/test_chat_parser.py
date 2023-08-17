from importlib import import_module
import pytest
import json
import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from DB.models import Groups

# TODO: make dynamic
INVALID_JSON = "invalid json"
DUMMY_USER_ID = "123456789"


@pytest.fixture
def chats_json():
    file_path = os.path.join(os.path.dirname(__file__), "dummy_chats.json")
    with open(file_path) as json_file:
        data = json.load(json_file)
    return data


@pytest.fixture(scope="module")
def test_app():
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DB_URL")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    with app.app_context():
        db = SQLAlchemy(app)
        import_models()  # Dynamically import the models
        db.create_all()

        yield app

        db.session.remove()
        db.drop_all()


@pytest.fixture(scope="module")
def chats_parser(chats_json):
    DUMMY_USER_ID = "your_dummy_user_id"  # Replace with your dummy user ID
    parser = ChatsParser(chats_json, DUMMY_USER_ID)
    return parser


# imports module dynamically to avoid circulair imports
def import_models():
    model_module = import_module("DB.models")
    for attribute_name in dir(model_module):
        attribute = getattr(model_module, attribute_name)
        if hasattr(attribute, "__tablename__"):
            globals()[attribute_name] = attribute


# Tests that file is retrived & valid
def test_json_data(chats_json):
    assert isinstance(chats_json, list)
    assert len(chats_json) > 0


def test_db_instance_started(test_app):
    with test_app.app_context():
        # Access the db instance
        from app import db

        assert isinstance(db, SQLAlchemy)


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
        parser = ChatsParser(invalid_json, DUMMY_USER_ID)
        parser.parse()
    except Exception as e:
        assert e == INVALID_JSON


# check that for each json obj an data class 'chats' instance is create with valid data
def test_chat_data_class_creation(chats_parser):
    chats = chats_parser.create_chats()
    assert len(chats) == len(chats_json)
    assert chats[0].user_id == DUMMY_USER_ID


# recive json chat obj return chat obj with valid user id
def test_succseful_create_chat_from_chat_json(json_chat, chats_parser):
    chat = chats_parser.create_chat(json_chat)
    assert chat.user_id == DUMMY_USER_ID
    assert chat.group_id == json_chat["group_id"]


# invalid chat json
def test_failed_create_chat_from_chat_json(json_chat, chats_parser):
    try:
        chat = chats_parser.create_chat(json_chat)
    except Exception as e:
        assert e == INVALID_JSON


# Test creates DB records from chats data class
def test_create_db_record_from_chat_class(chats_parser):
    chats = create_dummy_chats_data_class()
    chats_parser.create_db_records(chats)
    records_with_user_id = Groups.query.filter_by(user_id=DUMMY_USER_ID).all()
    assert len(records_with_user_id) == len(chats)


# Check parse summary return logical info
def test_parser_summary(chats_parser):
    len_data_variables, len_json = 10, 10
    summary = chats_parser.summary(len_data_variables, len_json, DUMMY_USER_ID)
    assert summary.total_records_created == len_data_variables
    assert summary.total_records_failed == 0
    assert summary.user_id == DUMMY_USER_ID
