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
    @jwt_required()
    def put(self, id_task):
        print('tarea', id_task)
        task = db.session.query(Task).filter(Task.id == id_task).first()
        task.new_format=request.values.get('newFormat')
        task.estado=TaskStatus.UPLOADED

        file_path=os.path.join(f'{CONVERTED_FOLDER}', f'{task.id}.{task.new_format.lower()}')
        if task.estado==TaskStatus.PROCESSED:
            if os.path.exists(file_path):
                 os.remove(file_path)

        db.session.add(task)
        db.session.commit()
        return task_scheme.dump(task)

    @jwt_required()
    def get(self, id_task):
        print('tarea-->', id_task)
        task = db.session.query(Task).filter(Task.id == id_task).first()
        if task:
            return task_scheme.dump(task)
        else:
            return {},404

    @jwt_required()
    def delete(self, id_task):
        task = db.session.query(Task).filter(Task.id == id_task).delete()
        db.session.commit()
        return {},404

