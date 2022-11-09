import io
import logging
import os

from flask import send_file
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


def get_file(task,request_file):
    try:
        if request_file == 'original':
            file_path = os.path.join(f'{CONVERTED_FOLDER}', f'{task.id}.{task.new_format.lower()}')
            print(f'Descargando archivo:{file_path}')
            return read_file(file_path, task.new_file)
        elif request_file == 'converted':
            if task.estado == TaskStatus.PROCESSED:
                file_path = os.path.join(f'{UPLOAD_FOLDER}', f'{task.id}.{task.format.lower()}')
                print(f'Descargando archivo:{file_path}')
                return read_file(file_path, task.file)
            else:
                abort(404)
        else:
            abort(404)
    except FileNotFoundError:
        abort(404)


class VistaFiles(Resource):
    @jwt_required()
    def get(self, filename):
        logging.info(f'DOWNLOAD: file--> {filename}')
        task = db.session.query(Task).filter(Task.file == filename).first()
        request_file = 'original'
        if task:
            '''Archivo sin convertir'''
        else:
            task = db.session.query(Task).filter(Task.new_file == filename).first()
            request_file = 'converted'
            '''Archivo convertido'''

        if task:
            return get_file(task, request_file)
        else:
            return {},404
