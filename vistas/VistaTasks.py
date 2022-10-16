import datetime

from flask_jwt_extended import  jwt_required, get_jwt_identity
from env import ALLOWED_EXTENSIONS, UPLOAD_FOLDER
from modelos import Task, db, Usuario, TaskSchema
from flask_restful import Resource
from sqlalchemy import desc, asc
import os
from flask import request
from werkzeug.utils import secure_filename

from tareas import encolar

task_scheme = TaskSchema()

def _allowed_file(filename):
    return '.' in filename and (filename.rsplit('.', 1)[1].upper() in ALLOWED_EXTENSIONS)


class VistaTasks(Resource):

    @jwt_required()
    def post(self):
        return {},404

    @jwt_required()
    def get(self):
        return {},404
