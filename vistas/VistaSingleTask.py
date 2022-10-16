from flask_jwt_extended import  jwt_required, get_jwt_identity
from env import ALLOWED_EXTENSIONS, CONVERTED_FOLDER, UPLOAD_FOLDER
from modelos import Task, db, Usuario, UsuarioSchema, TaskSchema, TaskStatus
from flask_restful import Resource
from sqlalchemy import  desc, asc
import os
from flask import request
from werkzeug.utils import secure_filename

task_scheme = TaskSchema()


def _allowed_file(filename):
    return '.' in filename and (filename.rsplit('.', 1)[1].upper() in ALLOWED_EXTENSIONS)


class VistaSingleTask(Resource):
    @jwt_required
    def put(self, id_task):
        return {},404

    @jwt_required
    def get(self, id_task):

            return {},404

    @jwt_required
    def delete(self, id_task):

        return {},404

