from flask import Blueprint
from .views import (
    list_create_update_destroy_tasks,
    create_user,
    login,
    logout,
    protected,
)

tasks = Blueprint("tasks", __name__)
tasks.route("/api/tasks", methods=["GET", "POST", "PATCH", "DELETE"])(
    list_create_update_destroy_tasks
)
tasks.route("/api/register", methods=["POST"])(create_user)
tasks.route("/api/login", methods=["POST"])(login)
tasks.route("/api/logout", methods=["GET"])(logout)
tasks.route("/api/who-am-i", methods=["GET"])(protected)
