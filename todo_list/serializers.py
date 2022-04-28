from pyexpat import model
from xml.etree.ElementInclude import include
from flask_marshmallow import Marshmallow
from .models import Tasks

ma = Marshmallow()


class TaskSchema(ma.Schema):
    class Meta:
        fields = "id", "title", "status", "user_id"
        model = Tasks
        include_fk = True


task_schema = TaskSchema()
tasks_schema = TaskSchema(many=True)
