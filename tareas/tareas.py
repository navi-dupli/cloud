import datetime
import logging
import os
import smtplib
import traceback

from celery import Celery
from celery.signals import task_postrun
from pydub import AudioSegment

from build import create_app
from env import REDIS_SERVER, REDIS_PORT, UPLOAD_FOLDER, CONVERTED_FOLDER, MAIL_NOTIFICATION_ENABLED
from modelos import db, Task, TaskStatus, Usuario, TaskSchema
from flask_mail import Mail
from flask_mail import Message

broker = f'redis://{REDIS_SERVER}:{REDIS_PORT}/0'


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

celery_app = make_celery(app)
mail = Mail(app)


def convert_file(json_task):
    format = json_task['format'].lower()
    new_format = json_task['new_format'].lower()
    convert_format = new_format
    if new_format == 'aac':
        convert_format = 'adts'
    if new_format == 'wma':
        convert_format = 'asf'
    given_audio = AudioSegment.from_file(os.path.join(UPLOAD_FOLDER, f'{json_task["id"]}.{format}'),
                                         format=format)
    given_audio.export(os.path.join(CONVERTED_FOLDER, f'{json_task["id"]}.{new_format}'), format=convert_format)

    logging.info(f'TASK:{json_task["id"]} - Convirtiendo archivo : {json_task["file"]}')
    return True


def send_mail(recipient, file_name):
    if MAIL_NOTIFICATION_ENABLED == 'TRUE':
        msg = Message('Conversión del archivo exitosa', sender='cloudteam35@gmail.com', recipients=[recipient])
        msg.body = f'El archivo {file_name} fue convertido exitosamente'
        mail.send(msg)
    return True


@celery_app.task(name="convertir-archivo")
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
                send_mail(usuario.correo, task.file)
                logging.info(f'TASK:{task.id} - Enviando correo a: {usuario.correo}')
            except Exception as e:
                logging.error(traceback.format_exc())



@task_postrun.connect()
def close_session(*args, **kwargs):
    print("CLOSE")
    # db.session.remove()
