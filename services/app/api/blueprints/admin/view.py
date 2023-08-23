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
from ..database.crud.admin import (
    create_admin, get_admin, get_admin_by_email, get_admins
)
from flasgger import swag_from
from flask import Blueprint, request
from flask_jwt_extended import jwt_required
from ..database.models.user import User
from ..database.database import get_db
from pydantic import ValidationError
from jwt import ExpiredSignatureError, InvalidTokenError
from http import HTTPStatus


admin = Blueprint("admin", __name__) 


@swag_from("./docs/register.yml", endpoint="admin.register", methods=["POST"])
@admin.route("/register", methods=["POST"])
def register():
    admin_data = UserCreate(**request.json)
    if get_admin_by_email(email=admin_data.email_address, session=get_db):
        return {'Error': f'Admin with email address {admin_data.email_address} already exists.'}, HTTPStatus.CONFLICT
    user = create_admin(admin_data=admin_data, session=get_db)
    resp = UserCreatedSchema(
        first_name=user.first_name,
        last_name=user.last_name,
        email_address=user.email_address,
        id=user.id,
        activation_token=User.encode_auth_token(user.id)
    )
    return resp.model_dump_json(indent=4), HTTPStatus.CREATED


@admin.route("/get", methods=["GET"])
# @admin_token_required
@swag_from("./docs/get.yml", endpoint="admin.get", methods=["GET"])
def get():
    try:
        admin_data = GetUser(user_id=request.args.get('user_id'))
    except ValidationError:
        return {'error': 'Invalid input: you probably did not include the admin id.'}, HTTPStatus.BAD_REQUEST
    user = get_admin(session=get_db, admin_data=admin_data)
    if user:
        resp = UserSchema(
            first_name=user.first_name,
            last_name=user.last_name,
            email_address=user.email_address,
            id=user.id
        )
        return resp.model_dump_json(indent=4), HTTPStatus.OK
    
    return {'Error':f'No admin with id {admin_data.user_id}'}, HTTPStatus.NOT_FOUND


@admin.route("/list_all", methods=["GET"])
# @admin_token_required
@swag_from("./docs/admins.yml", endpoint="admin.list_all", methods=["GET"])
def list_all():
    offset: str = request.args.get('offset')
    limit: str = request.args.get('limit')
    admins = get_admins(get_db, GetUsers(offset=offset, limit=limit))
    admins = [
        UserSchema(
            first_name=admin.first_name,
            last_name=admin.last_name,
            email_address=admin.email_address,
            id=admin.id
            ).model_dump()
        for admin in admins
    ]
    return admins, HTTPStatus.OK