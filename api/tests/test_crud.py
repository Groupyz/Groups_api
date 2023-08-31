import pytest
from app import app, db
from DB.models import Groups
from DB.dbHandler import *
from routes import GROUP_PATH


@pytest.fixture(scope="module")
def test_client():
    flask_app = app
    flask_app.config["TESTING"] = True

    with flask_app.test_client() as testing_group:
        with flask_app.app_context():
            yield testing_group
            delete_test_groups(1)


def test_get_all_groups(test_client):
    groups = create_2_test_groups()
    user_id = groups[0].user_id
    response = test_client.get(f'/{GROUP_PATH}/{user_id}')
    delete_test_groups(user_id)
    assert response.status_code == 200 and "groups" in response.text


def create_2_test_groups():
    new_group_1 = Groups(  user_id = 1,
                        group_id = "1",
                        group_name = "test1")
    new_group_2 = Groups(  user_id = 1,
                        group_id = "2",
                        group_name = "test2")
    db.session.add(new_group_1)
    db.session.add(new_group_2)
    db.session.commit()

    created_groups = []
    created_groups.append(new_group_1)
    created_groups.append(new_group_2)

    return created_groups


def delete_test_groups(user_id):
    Groups.query.filter_by(user_id=user_id).delete()
    db.session.commit()