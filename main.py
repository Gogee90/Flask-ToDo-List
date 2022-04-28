from re import A
from flask import Flask
from .todo_list.routes import tasks
from .todo_list.models import db
from .todo_list.views import jwt
from .todo_list.serializers import ma
from flask_migrate import Migrate


app = Flask(__name__)
migrate = Migrate(app, db, compare_type=True)
app.config[
    "SQLALCHEMY_DATABASE_URI"
] = "postgresql://todoadmin:todopass@localhost/tododb"
app.config["SECRET_KEY"] = "super-secret"
app.config["JWT_BLACKLIST_ENABLED"] = True
app.config["JWT_BLACKLIST_TOKEN_CHECKS"] = ["access", "refresh"]
app.register_blueprint(tasks)
db.init_app(app)
jwt.init_app(app)
ma.init_app(app)

if __name__ == "__main__":
    app.run(debug=True)
