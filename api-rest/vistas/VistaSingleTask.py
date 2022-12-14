import logging

from flask_jwt_extended import jwt_required
from env import ALLOWED_EXTENSIONS, CONVERTED_FOLDER,PROJECT_ID,TOPIC
from modelos import Task, db, TaskSchema, TaskStatus
from flask_restful import Resource
from flask import request
from utils import StorageUtils
from tareas import  publish_messages

task_schema = TaskSchema()


def _allowed_file(filename):
    return '.' in filename and (filename.rsplit('.', 1)[1].upper() in ALLOWED_EXTENSIONS)


class VistaSingleTask(Resource):
    @jwt_required()
    def put(self, id_task):
        logging.info(f'PUT: tarea--> {id_task}')
        task = db.session.query(Task).filter(Task.id == id_task).first()
        task.new_format = request.values.get('newFormat')
        task.estado = TaskStatus.UPLOADED

        file_path = f'{CONVERTED_FOLDER}{task.id}.{task.new_format}'
        if task.estado == TaskStatus.PROCESSED:
            print(f'Eliminando archivo {task.id}:{file_path}')
            StorageUtils.delete(file_path)

        db.session.add(task)
        db.session.commit()
        publish_messages(PROJECT_ID,TOPIC, task_schema.dump(task))
        logging.info(f'TASK:{task.id} - Tarea creada y encolada ')
        return task_schema.dump(task)

    @jwt_required()
    def get(self, id_task):
        logging.info(f'GET: tarea--> {id_task}')
        task = db.session.query(Task).filter(Task.id == id_task).first()
        if task:
            return task_schema.dump(task)
        else:
            return {}, 404

    @jwt_required()
    def delete(self, id_task):
        logging.info(f'DELETE: tarea--> {id_task}')
        task = db.session.query(Task).filter(Task.id == id_task).delete()
        db.session.commit()
        return {}, 200
