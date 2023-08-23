from . import (
    UserCreate, UserCreated, GetUser, GetUsers, PasswordReset, RequestPasswordReset
)
from pydantic import ValidationError
import pytest


def test_user_create_missing_email(generate_user_no_email):
    with pytest.raises(ValidationError):
        UserCreate(**generate_user_no_email)
    
def test_user_create(generate_user_data):
    user_schema = UserCreate(**generate_user_data)
    assert user_schema is not None
    assert user_schema.role == 'user'
    assert user_schema.activated is False