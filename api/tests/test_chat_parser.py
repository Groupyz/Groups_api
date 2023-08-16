import pytest
import json
import os

@pytest.fixture
def chats_json():
    file_path = os.path.join(os.path.dirname(__file__), "dummy_chats.json")
    with open(file_path) as json_file:
        data = json.load(json_file)
    return data

# Tests that file is retrived & valid
def test_json_data(chats_json):
    assert isinstance(chats_json, list)
    assert len(chats_json) > 0
