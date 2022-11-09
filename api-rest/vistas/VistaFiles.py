import io
import logging
import os

from flask import  send_file
from flask_jwt_extended import jwt_required

from env import CONVERTED_FOLDER, UPLOAD_FOLDER
from modelos import Task, db, UsuarioSchema, TaskSchema, TaskStatus
from flask_restful import Resource, abort
from utils import StorageUtils



def read_file(file_path, file_name):
    file = StorageUtils.read(file_path)
    return send_file(
        io.BytesIO(file),
        as_attachment=True,
        attachment_filename=f'{file_name}'
    )


def get_file(task):
    try:
        if task.estado == TaskStatus.PROCESSED:
            file_path = os.path.join(f'{CONVERTED_FOLDER}', f'{task.id}.{task.new_format.lower()}')
            return read_file(file_path, task.new_file)
        elif task.estado == TaskStatus.UPLOADED:
            file_path = os.path.join(f'{UPLOAD_FOLDER}', f'{task.id}.{task.format.lower()}')
            return read_file(file_path, task.file)
        else:
            abort(404)
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

        return get_file(task)
