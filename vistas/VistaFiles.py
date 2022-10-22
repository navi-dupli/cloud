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
    @jwt_required()
    def get(self, filename):
        task = db.session.query(Task).filter(Task.file == filename).first()

        '''Download file'''
        try:
            if task.estado == TaskStatus.PROCESSED:
                file_path = os.path.join(f'{CONVERTED_FOLDER}', f'{task.id}.{task.new_format.lower()}')
                if os.path.exists(file_path):
                    return send_from_directory(CONVERTED_FOLDER, f'{task.id}.{task.new_format.lower()}', as_attachment=True)
            elif task.estado == TaskStatus.UPLOADED:
                file_path = os.path.join(f'{UPLOAD_FOLDER}', f'{task.id}.{task.new_format.lower()}')
                if os.path.exists(file_path):
                    return send_from_directory(UPLOAD_FOLDER, f'{task.id}.{task.new_format.lower()}', as_attachment=True)
            else:
                return {}, 404
        except FileNotFoundError:
            abort(404)
