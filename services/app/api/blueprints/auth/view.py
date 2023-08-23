from flasgger import swag_from
from flask import Blueprint, request
from flask_jwt_extended import jwt_required
from flask_jwt_extended import create_access_token, create_refresh_token
from http import HTTPStatus

from ..database.schema.user import (
    UserCreate, GetUser, GetUsers, User as UserSchema, UserCreated as UserCreatedSchema,
    ActivateUser, LoginUser, LoggedInUser, RequestPasswordReset, RequestPasswordResetToken,
    PasswordReset
)
from ..database.crud.user import (
    create_user, get_user_by_email, get_user, get_users, delete_user, user_account_active,
    activate_user_account, loggin_user, generate_password_reset_token, password_repeated,
    reset_password
)
from ..database.models.user import User
from ..database.database import get_db
from pydantic import ValidationError
from jwt import ExpiredSignatureError, InvalidTokenError


auth = Blueprint("auth", __name__)

@auth.route("/register", methods=["POST"])
@swag_from("./docs/register.yml", endpoint="auth.register_client", methods=["POST"])
def register_client():
    try:
        user_data = UserCreate(**request.json) 
    except ValidationError:
        return {'Error': 'The data provided is invalid or incomplete!'}, HTTPStatus.BAD_REQUEST
    if get_user_by_email(email=user_data.email_address, session=get_db):
        return {'Error': f'User with email address {user_data.email_address} already exists.'}, HTTPStatus.CONFLICT
    user = create_user(user_data=user_data, session=get_db) 
    resp = UserCreatedSchema(
        first_name=user.first_name,
        last_name=user.last_name,
        email_address=user.email_address,
        id=user.id,
        activation_token=User.encode_auth_token(user.id)
    )
    return resp.model_dump_json(indent=4), HTTPStatus.CREATED


@auth.route("/get", methods=["GET"])
# @jwt_required()
@swag_from("./docs/get.yml", endpoint="auth.get_client", methods=["GET"])
def get_client():
    try:
        user_data = GetUser(user_id=request.args.get('user_id'))
    except ValidationError:
        return {'error': 'Invalid input: you probably did not include the user id.'}, HTTPStatus.BAD_REQUEST
    user = get_user(session=get_db, user_data=user_data)
    if user:
        resp = UserSchema(
            first_name=user.first_name,
            last_name=user.last_name,
            email_address=user.email_address,
            id=user.id
        )
        return resp.model_dump_json(indent=4), HTTPStatus.OK
    
    return {'Error':f'No user with id {user_data.user_id}'}, HTTPStatus.NOT_FOUND

@auth.route("/update", methods=["PUT"])
# @jwt_required()
@swag_from("./docs/update.yml", endpoint="auth.update_client", methods=["PUT"])
def update_client():
    return {'success': 'registered'}, HTTPStatus.CREATED


@auth.route("/delete", methods=["DELETE"])
# @admin_token_required
@swag_from("./docs/delete.yml", endpoint="auth.delete_client", methods=["DELETE"])
def delete_client():
    try:
        user_data = GetUser(user_id=request.args.get('user_id'))
    except ValidationError:
        return {'error': 'Invalid input: you probably did not include the user id.'}, HTTPStatus.BAD_REQUEST
    user = get_user(session=get_db, user_data=user_data)
    if not user:
        return {'Error': f'User with id {user_data.user_id} does not exists'}, HTTPStatus.NOT_FOUND
    user = delete_user(get_db, GetUser(user_id=request.args.get('user_id')))
    resp = UserSchema(
        first_name=user.first_name,
        last_name=user.last_name,
        email_address=user.email_address,
        id=user.id
    )
    return resp.model_dump_json(indent=4), HTTPStatus.OK


@auth.route("/users", methods=["GET"])
# @admin_token_required
@swag_from("./docs/users.yml", endpoint="auth.list_all", methods=["GET"])
def list_all():
    offset: str = request.args.get('offset')
    limit: str = request.args.get('limit')
    users = get_users(get_db, GetUsers(offset=offset, limit=limit))
    users = [
        UserSchema(
            first_name=user.first_name,
            last_name=user.last_name,
            email_address=user.email_address,
            id=user.id
            ).model_dump()
        for user in users
    ]
    return users, HTTPStatus.OK


@swag_from("./docs/activate.yml", endpoint="auth.activate_account", methods=["GET"])
@auth.route("/activate", methods=["GET"])
def activate_account():
    """Activate User account."""
    try:
        activation_data = ActivateUser(**request.args)
    except ValidationError:
        return {'Error': 'Missing token or user id.'}, HTTPStatus.BAD_REQUEST
    if not get_user(user_data=GetUser(user_id=activation_data.user_id), session=get_db):
        return {'Error': f'User with id {activation_data.user_id} does not exists'}, HTTPStatus.NOT_FOUND
    if user_account_active(session=get_db, user_data=GetUser(user_id=activation_data.user_id)):
        return {'Error': f'Account with id {activation_data.user_id} is already activated.'}, HTTPStatus.FORBIDDEN
    try:
        activate_user_account(session=get_db, activation_data=activation_data)
    except (ExpiredSignatureError, InvalidTokenError):
        return {'Error': 'Invalid or Expired activation token.'}, HTTPStatus.FORBIDDEN
    else:
        return {'Success': f'Account with id {activation_data.user_id} activated!'}, HTTPStatus.OK

@swag_from("./docs/login.yml", endpoint="auth.login_client", methods=["POST"])
@auth.route("/login", methods=["POST"])
def login_client():
    """Login a registered, confirmed client."""
    try:
        login_data = LoginUser(**request.json)
    except ValidationError:
        return {'Error': 'Missing password and or email address.'}, HTTPStatus.BAD_REQUEST
    user = get_user_by_email(email=login_data.email_address, session=get_db)
    if user:
        if not user_account_active(session=get_db, user_data=GetUser(user_id=user.id)):
            return {'Error': f'Account with email address {login_data.email_address} is not activated.'}
    try:
        loggin_user(session=get_db, login_data=login_data)
    except ValueError as e:
        return {'Error': 'Invlaid email address and or password.'}, HTTPStatus.UNAUTHORIZED
    else:
        resp = LoggedInUser(
            email_address=login_data.email_address,
            access_token=create_access_token(user.id),
            refresh_token=create_refresh_token(user.id)
        ).model_dump_json()
        return resp, HTTPStatus.OK

@swag_from(
    "./docs/password_reset_request.yml",
    endpoint="auth.request_client_password_reset",
    methods=["GET"],
)
@auth.route("/request_password_reset", methods=["GET"])
def request_client_password_reset():
    """Request a client password reset."""
    try:
        password_reset_request = RequestPasswordReset(**request.args)
    except ValidationError:
        return {'Error': 'Missing user id and or email address.'}, HTTPStatus.BAD_REQUEST
    user_by_id = get_user(session=get_db, user_data=GetUser(user_id=password_reset_request.user_id))
    user_by_email = get_user_by_email(email=password_reset_request.email_address, session=get_db)
    if not user_by_id or not user_by_email or not user_by_email.id == user_by_id.id:
        return {'Error': f'User with id {password_reset_request.user_id} and or email {password_reset_request.email_address} does not exists'}, HTTPStatus.NOT_FOUND
    if not user_account_active(session=get_db, user_data=GetUser(user_id=password_reset_request.user_id)):
        return {'Error': 'You cannot reset the password for an account that has not been activated.'}
    password_reset_token = generate_password_reset_token(session=get_db, reset_password_request=password_reset_request)
    resp = RequestPasswordResetToken(**password_reset_token).model_dump_json()
    return resp, HTTPStatus.OK


@swag_from("./docs/reset_password.yml", endpoint="auth.reset_client_password", methods=["POST"])
@auth.route("/reset_password", methods=["POST"])
def reset_client_password():
    """Reset a client password."""
    try:
        password_reset = PasswordReset(**request.json)
    except ValidationError:
        return {'Error': 'Invalid password rest data.'}, HTTPStatus.BAD_REQUEST
    if password_reset.password != password_reset.confirm_password:
        return {'Error': 'The two passwords do not match'}, HTTPStatus.BAD_REQUEST 
    user = get_user_by_email(email=password_reset.email_address, session=get_db)
    if not user:
        return {'Error': f'User with email address {password_reset.email_address} does not exist.'}, HTTPStatus.CONFLICT
    if not user_account_active(session=get_db, user_data=GetUser(user_id=user.id)):
        return {'Error': f'You cannot rest the password for an unactivated account.'}
    
    if password_repeated(session=get_db, password_reset=password_reset):
        return {'Error': 'You have used this password before.'}
    try:
        reset_password(session=get_db, password_reset=password_reset)
    except (ExpiredSignatureError, InvalidTokenError):
        return {'Error': 'Invalid or Expired password reset token.'}, HTTPStatus.FORBIDDEN
    else:
        return {'Success': f'Password for account with email {password_reset.email_address} succesfully changed.'}


@auth.route("/refresh_token", methods=["POST"])
@swag_from("./docs/refresh_token.yml", endpoint="auth.refresh_token", methods=["POST"])
def refresh_token():
    """Refresh an expired token."""
    return {'success': 'registered'}, HTTPStatus.CREATED
