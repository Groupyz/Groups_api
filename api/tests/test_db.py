import pytest
from app import app, db
from DB.models import Groups
from DB.dbHandler import generate_id


# delete test data after end of test
@pytest.fixture(scope="session", autouse=True)
def delete_remaining_data():
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
        user_id=generate_id(), group_id="1", group_name="Surviving the Sadna!"
    )
    return new_data


# these tests are for testing the primary key, which is: user_id + group_id
def test_same_user_diff_groups():
    with app.app_context():
        group_1 = Groups(user_id=generate_id(), group_id="10", group_name="Surviving the Sadna!")
        
        group_2 = Groups(user_id=group_1.user_id, group_id="20", group_name="Surviving the Sadna!")

        db.session.add(group_1)
        db.session.add(group_2)
        db.session.commit()

        group_1_data = Groups.query.filter_by(group_id="10")
        group_2_data = Groups.query.filter_by(group_id="20")

        db.session.delete(group_1)
        db.session.delete(group_2)
        db.session.commit()

        assert (group_1_data and group_2_data) is not None


def test_same_users_same_groups():
    with app.app_context():
        with pytest.raises(Exception) as error:
            group_1 = Groups(user_id=generate_id(), group_id="30", group_name="Surviving the Sadna!")
            
            group_2 = Groups(user_id=group_1.user_id, group_id="30", group_name="Surviving the Sadna!")

            db.session.add(group_1)
            db.session.add(group_2)
            db.session.commit()

            assert "duplicate key" in error


def test_group_id_type():
     with app.app_context():
        try:
            group = Groups(user_id=generate_id(), group_id="40", group_name="Surviving the Sadna!")
            
            db.session.add(group)
            db.session.commit()

        except ValueError as error:
            assert "group_id" in str(error)
          
  


