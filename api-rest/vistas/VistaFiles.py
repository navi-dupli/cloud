import logging
import os

from flask import  send_from_directory
from flask_jwt_extended import jwt_required

from env import CONVERTED_FOLDER, UPLOAD_FOLDER
from modelos import Task, db, UsuarioSchema, TaskSchema, TaskStatus
from flask_restful import Resource, abort

usuario_schema = UsuarioSchema()
task_scheme = TaskSchema()


def _getFile(task):
    try:
        if task.estado == TaskStatus.PROCESSED:
            file_path = os.path.join(f'{CONVERTED_FOLDER}', f'{task.id}.{task.new_format.lower()}')
            if os.path.exists(file_path):
                return send_from_directory(CONVERTED_FOLDER, f'{task.id}.{task.new_format.lower()}',
                                           as_attachment=True)
        elif task.estado == TaskStatus.UPLOADED:
            file_path = os.path.join(f'{UPLOAD_FOLDER}', f'{task.id}.{task.format.lower()}')
            if os.path.exists(file_path):
                return send_from_directory(UPLOAD_FOLDER, f'{task.id}.{task.format.lower()}',
                                           as_attachment=True)
        else:
            return {}, 404
    except FileNotFoundError:
        abort(404)


class VistaFiles(Resource):
    @jwt_required()
    def get(self, filename):
        logging.info(f'DOWNLOAD: file--> {filename}')
        task = db.session.query(Task).filter(Task.file == filename).first()
        if task:
            '''Archivo sin convertir'''
        else:
            task = db.session.query(Task).filter(Task.new_file == filename).first()
            '''Archivo convertido'''

        return _getFile(task)
