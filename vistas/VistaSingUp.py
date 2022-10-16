import re

from flask import request
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity

from modelos import Task ,db, Usuario, UsuarioSchema, TaskSchema
from flask_restful import Resource
from sqlalchemy import or_, desc, asc

usuario_schema = UsuarioSchema()
task_scheme = TaskSchema()


class VistaSingUp(Resource):
    def post(self):
        return {},404





