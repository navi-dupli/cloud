import os
import re

from flask import request, send_file, send_from_directory
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity

from env import CONVERTED_FOLDER, UPLOAD_FOLDER
from modelos import Task, db, Usuario, UsuarioSchema, TaskSchema, TaskStatus
from flask_restful import Resource, abort
from sqlalchemy import or_, desc, asc

usuario_schema = UsuarioSchema()
task_scheme = TaskSchema()


class VistaFiles(Resource):
    @jwt_required
    def get(self, filename):
            abort(404)
