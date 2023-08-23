from .. import UserCreate, get_db, create_user
from datetime import datetime

def test_create_user():
    user_data = {
        'first_name': 'first_name',
        'last_name': 'last_name',
        'email_address': 'first_name_last_name@gmail.com',
        'password': 'password'
    }
    user_schema = UserCreate(**user_data)
    user = create_user(user_data=user_schema, session=get_db)
    assert user is not None
    assert user.id is not None
    assert user.password != user_data['password']
    assert user.email_address == user_data['email_address']
    assert user.first_name == user_data['first_name']
    assert user.last_name == user_data['last_name']
    assert user.role == 'user'
    assert user.activated is False
    assert user.registration_date is not None
    assert user.registration_date < datetime.utcnow()