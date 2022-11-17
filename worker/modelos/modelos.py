from flask_sqlalchemy import SQLAlchemy
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from marshmallow import fields
import enum

from sqlalchemy import func

db = SQLAlchemy()


class TaskStatus(enum.Enum):
    UPLOADED = "UPLOADED"
    PROCESSED = "PROCESSED"
    INPROGRESS = "INPROGRESS"


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    file = db.Column(db.String(512))
    new_file = db.Column(db.String(512))
    timestamp = db.Column(db.DateTime(timezone=True), default=func.now())
    format = db.Column(db.String(10))
    new_format = db.Column(db.String(10))
    estado = db.Column(db.Enum(TaskStatus), default=TaskStatus.UPLOADED)
    usuario = db.Column(db.Integer, db.ForeignKey("usuario.id"))
    processed_timestamp = db.Column(db.DateTime(timezone=True))



class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50))
    password = db.Column(db.String(50))
    correo = db.Column(db.String(150))
    tareas = db.relationship('Task', cascade='all, delete, delete-orphan')


class EnumADiccionario(fields.Field):
    def _serialize(self, value, attr, obj, **kwargs):
        if value is None:
            return None
        return value.value


class UsuarioSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Usuario
        include_relationships = True
        load_instance = True
        exclude = ("password", "tareas")


class TaskSchema(SQLAlchemyAutoSchema):
    usuario = fields.Nested(UsuarioSchema())
    estado = EnumADiccionario(attribute="estado")

    class Meta:
        model = Task
        include_relationships = True
        load_instance = True
