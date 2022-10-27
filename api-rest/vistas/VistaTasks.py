import datetime
import logging

from flask_jwt_extended import jwt_required, get_jwt_identity
from env import ALLOWED_EXTENSIONS, UPLOAD_FOLDER
from modelos import Task, db, Usuario, TaskSchema
from flask_restful import Resource
from sqlalchemy import desc, asc
import os
from flask import request
from werkzeug.utils import secure_filename

from tareas import encolar

task_schema = TaskSchema()


def _allowed_file(filename):
    return '.' in filename and (filename.rsplit('.', 1)[1].upper() in ALLOWED_EXTENSIONS)


class VistaTasks(Resource):

    @jwt_required()
    def post(self):
        current_user_id = get_jwt_identity()
        if 'fileName' not in request.files:
            return {"ok": False, "mensaje": "El request no contiene el archivo"}
        file = request.files['fileName']
        if file.filename == '':
            return {"ok": False, "mensaje": "El request no contiene el archivo"}
        if file and _allowed_file(file.filename):
            filename = secure_filename(file.filename)

            current_format = filename.rsplit('.', 1)[1].upper()
            task_new = Task(file=f'{datetime.datetime.now().timestamp()}__{file.filename}',
                            format=current_format,
                            new_format=request.form["newFormat"].upper(),
                            usuario=current_user_id)
            db.session.add(task_new)
            db.session.commit()

            file.save(os.path.join(UPLOAD_FOLDER, f'{task_new.id}.{current_format.lower()}'))
            encolar.delay(task_new.id)
            logging.info(f'TASK:{task_new.id} - Tarea modificada y encolada ')
            return task_schema.dump(task_new)
        else:
            return {"ok": False, "mensaje": "El archivo no esta permitido"}

    @jwt_required()
    def get(self):
        current_user_id = get_jwt_identity()
        order = 0
        max = 10
        if request.values.get("order"):
            order = request.values.get("order")

        if request.values.get("max"):
            max = request.values.get("max")
        tasks = []
        if order == 0:
            tasks = db.session.query(Task).join(Usuario).filter(Usuario.id == current_user_id).order_by(
                asc(Task.id)).limit(max).all()
        else:
            tasks = db.session.query(Task).join(Usuario).filter(Usuario.id == current_user_id).order_by(
                desc(Task.id)).limit(max).all()
        return [task_schema.dump(item) for item in tasks]
