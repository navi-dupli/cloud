import datetime
import io
import logging
import os
import traceback

from celery import Celery
from celery.signals import task_postrun
from pydub import AudioSegment

from build import create_app
from env import REDIS_SERVER, REDIS_PORT, UPLOAD_FOLDER, CONVERTED_FOLDER, MAIL_NOTIFICATION_ENABLED
from modelos import db, Task, TaskStatus, Usuario, TaskSchema
from flask_mail import Mail
from flask_mail import Message
from utils import StorageUtils

broker = f'redis://{REDIS_SERVER}:{REDIS_PORT}/0'


# broker = f'redis://localhost:6379/0'


def make_celery(app):
    celery = Celery(app.import_name, broker=broker)

    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery.Task = ContextTask
    return celery


app = create_app('Cloud_Converter_CELERY')

app_context = app.app_context()
app_context.push()
db.init_app(app)

celery = make_celery(app)
mail = Mail(app)


def convert_file(json_task):
    format = json_task['format'].lower()
    new_format = json_task['new_format'].lower()
    convert_format = new_format
    if new_format == 'aac':
        convert_format = 'adts'
    if new_format == 'wma':
        convert_format = 'asf'

    original_file_path = f'{UPLOAD_FOLDER}{json_task["id"]}.{format}'
    original_file_bytes = StorageUtils.read(original_file_path)
    original_file = io.BytesIO(original_file_bytes)

    given_audio = AudioSegment.from_file_using_temporary_files(file=original_file, format=format)

    new_file_path = f'{CONVERTED_FOLDER}{json_task["id"]}.{new_format}'
    new_file_bytes =  io.BytesIO()
    given_audio.export(new_file_bytes, format=convert_format)

    StorageUtils.save(new_file_path, new_file_bytes.getvalue())

    logging.info(f'TASK:{json_task["id"]} - Convirtiendo archivo : {json_task["file"]}')
    return True


def send_mail(recipient, file_name,task_id,mail):
    if MAIL_NOTIFICATION_ENABLED == 'TRUE':
        logging.info(f'TASK:{task_id} - Enviando correo a: {mail}')
        msg = Message('Conversión del archivo exitosa', sender='cloudteam35@gmail.com', recipients=[recipient])
        msg.body = f'El archivo {file_name} fue convertido exitosamente'
        mail.send(msg)
    return True


@celery.task(name="convertir-archivo")
def encolar(id_task):
    task = db.session.query(Task).filter(Task.id == id_task).first()
    if task:
        task_scheme = TaskSchema()
        json_task = task_scheme.dump(task)
        if convert_file(json_task):
            new_format = json_task['new_format'].lower()
            task.new_file = task.file.replace(f'.{task.format.lower()}', f'.{new_format.lower()}')
            task.estado = TaskStatus.PROCESSED
            task.processed_timestamp = datetime.datetime.now()
            db.session.add(task)
            db.session.commit()
            usuario = Usuario.query.get(task.usuario)
            try:
                send_mail(usuario.correo, task.file,task.id,usuario.correo)
            except Exception as e:
                logging.error(traceback.format_exc())


@task_postrun.connect()
def close_session(*args, **kwargs):
    print("CLOSE")
    # db.session.remove()
