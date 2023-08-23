import pytest
from . import User


@pytest.fixture(scope='module')
def generate_user_data():
    user_data = {
        'first_name': 'lyle',
        'last_name': 'okoth',
        'email_address': 'lyle@gmail.com',
        'password': 'password'
    }
    return user_data

@pytest.fixture(scope='module')
def generate_user_no_email():
    user_data = {
        'first_name': 'lyle',
        'last_name': 'okoth',
        'password': 'password'
    }
    return user_data

@pytest.fixture(scope='module')
def create_user(generate_user_data):
    user = User(**generate_user_data)
    return user