from .models import Tasks, User, db
from .serializers import task_schema, tasks_schema
from .decorators import error_message
from flask import jsonify
from flask import request
from flask_jwt_extended import (
    create_access_token,
    jwt_required,
    create_refresh_token,
    get_jwt,
    current_user,
)
import bcrypt
import datetime
from flask_jwt_extended import JWTManager


jwt = JWTManager()

blacklist = set()


@jwt.user_identity_loader
def user_identity_lookup(user):
    return user


@jwt.user_lookup_loader
def user_lookup_callback(_jwt_header, jwt_data):
    identity = jwt_data["sub"]
    return User.query.filter_by(username=identity).one_or_none()


@jwt.token_in_blocklist_loader
def check_if_token_in_blacklist(data, decrypted_token):
    jti = decrypted_token["jti"]
    return jti in blacklist


@error_message
@jwt_required()
def list_create_update_destroy_tasks():

    tasks = Tasks()

    if request.method == "POST":
        task = tasks.create(**request.json)
        task.user_id = current_user.id
        db.session.add(task)
        db.session.commit()
        return jsonify(task_schema.dump(task)), 200
    if request.method == "PATCH":
        task_to_update = tasks.patch(**request.json)
        db.session.commit()
        return jsonify(task_schema.dump(task_to_update)), 200
    if request.method == "DELETE":
        tasks.destroy(request.json["id"])
        db.session.commit()
        return jsonify({"id": request.json["id"]}), 200

    return jsonify(
        tasks_schema.dump(tasks.query.filter(Tasks.user_id == current_user.id))
    )


@error_message
def create_user():
    data = request.get_json()
    if data:
        salt = bcrypt.gensalt()
        encoded_password = data["password"].encode("utf-8")
        hashed_password = bcrypt.hashpw(encoded_password, salt).decode("utf8")
        new_user = User(
            username=data["username"], email=data["email"], password=hashed_password
        )
        db.session.add(new_user)
        db.session.commit()
        return jsonify(new_user.serialized_data), 200


@error_message
def login():

    auth_data = {}

    data = request.get_json()
    encoded_password = data["password"].encode("utf8")
    user = User.query.filter(User.username == data["username"]).first()
    elapsed_time = datetime.timedelta(minutes=40)
    if bcrypt.checkpw(encoded_password, user.password.encode("utf8")):
        auth_data["expires_in"] = str(elapsed_time)
        auth_data["refresh_token"] = create_refresh_token(
            identity=user.username, expires_delta=elapsed_time
        )
        auth_data["access_token"] = create_access_token(
            identity=user.username, expires_delta=elapsed_time
        )
        auth_data["token_type"] = "Bearer"
        return jsonify(auth_data), 200

    return jsonify({"error": "Credentials either wrong or were not provided!"}), 400


@error_message
@jwt_required()
def logout():
    jti = get_jwt()["jti"]
    blacklist.add(jti)
    return jsonify(()), 204


@error_message
@jwt_required()
def protected():
    return jsonify(
        id=current_user.id,
        full_name=current_user.email,
        username=current_user.username,
    )
