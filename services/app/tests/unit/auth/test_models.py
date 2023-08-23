from . import User
from datetime import datetime

def test_user():
    user = User(
        first_name='lyle',
        last_name='okoth',
        email_address='lyle@gmail.com',
        password='password'
    )
    assert user.id is None
    assert user.first_name == 'lyle'
    assert user.last_name == 'okoth'
    assert user.email_address == 'lyle@gmail.com'
    assert user.password == 'password'
    assert user.role == 'user'
    assert user.registration_date is not None
    assert user.registration_date < datetime.utcnow()
    assert user.activated is False
    
def test_user_password_encrypted():
    user = User(
        first_name='lyle',
        last_name='okoth',
        email_address='lyle@gmail.com',
        password=User.hash_password('password')
    )
    assert user.password != 'password'
    
def test_user_password_matches():
    user = User(
        first_name='lyle',
        last_name='okoth',
        email_address='lyle@gmail.com',
        password=User.hash_password('password')
    )
    assert user.check_password('password') is True
    