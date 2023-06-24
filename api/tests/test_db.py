import pytest
from app import app, db
from DB.models import Groups
from DB.dbHandler import generate_id


# delete test data after end of test
@pytest.fixture(scope="session", autouse=True)
def delete_remaining_users():
    yield
    with app.app_context():
        data = Groups.query.filter_by(group_name="Surviving the Sadna!").first()
        if data:
            db.session.delete(data)
            db.session.commit()


@pytest.fixture(scope="session")
def test_client():
    flask_app = app
    flask_app.config["TESTING"] = True

    with flask_app.test_client() as testing_client:
        with flask_app.app_context():
            yield testing_client


def test_create_data():
    with app.app_context():
        new_data = create_test_data()
        if new_data:
            db.session.add(new_data)
            db.session.commit()

            saved_data = Groups.query.filter_by(group_name="Surviving the Sadna!")
            assert saved_data is not None


def create_test_data():
    new_data = Groups(
        user_id=generate_id(), group_id=1, group_name="Surviving the Sadna!"
    )
    return new_data
