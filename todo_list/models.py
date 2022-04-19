from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import UUID
import uuid

db = SQLAlchemy(session_options={
    'expire_on_commit': False
})

class Tasks(db.Model):
    __tablename__ = "tasks"
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = db.Column(db.String(255))
    status = db.Column(db.String(100))
    user_id = db.Column(UUID(as_uuid=True), db.ForeignKey("users.id"))
    user = db.relationship("User", backref="tasks")
    
    @property
    def serialized_data(self):
        return {
            "id": self.id,
            "title": self.title,
            "status": self.status
        }
    
    def __repr__(self):
        return f"<Tasks: {self.title}>"
    
    
class User(db.Model):
    __tablename__ = "users"
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    username = db.Column(db.String(100), nullable=False, unique=True)
    email = db.Column(db.String(255), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)
    
    @property
    def serialized_data(self):
        return {"id": self.id, "username": self.username, "email": self.email, "password": self.password}
    
    def __repr__(self):
        return f"<User: {self.username}>"