from re import S
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import UUID
import uuid
from .mixins import CRUDMixin

db = SQLAlchemy(session_options={"expire_on_commit": False})


class Tasks(CRUDMixin, db.Model):
    __tablename__ = "tasks"
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = db.Column(db.String(255))
    status = db.Column(db.String(100))
    user_id = db.Column(UUID(as_uuid=True), db.ForeignKey("users.id"))
    user = db.relationship("User", backref="tasks")

    def __repr__(self):
        return f"<Tasks: {self.title}>"


class User(CRUDMixin, db.Model):
    __tablename__ = "users"
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    username = db.Column(db.String(100), nullable=False, unique=True)
    email = db.Column(db.String(255), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)

    def __repr__(self):
        return f"<User: {self.username}>"
