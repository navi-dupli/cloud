import os

from celery import Celery
from celery.signals import task_postrun
from pydub import AudioSegment

from env import REDIS_SERVER, REDIS_PORT, UPLOAD_FOLDER, CONVERTED_FOLDER
from modelos import db, Task, TaskStatus

celery_app = Celery('tasks', broker=f'redis://{REDIS_SERVER}:{REDIS_PORT}/0')


def convert_file(json_task):
    format = json_task['format'].lower()
    new_format = json_task['new_format'].lower()
    convert_format = new_format
    if new_format == 'acc':
        convert_format = 'adts'
    given_audio = AudioSegment.from_file(os.path.join(UPLOAD_FOLDER, f'{json_task["id"]}.{format}'),
                                         format=format)
    given_audio.export(os.path.join(CONVERTED_FOLDER, f'{json_task["id"]}.{new_format}'), format=convert_format)

    print('entra a convertir', json_task['id'])
    return True


def send_mail():
    return True


@celery_app.task(name="convertir-archivo")
def encolar(json_task):
    if convert_file(json_task):
        send_mail()
        new_format = json_task['new_format'].lower()
        task = db.session.query(Task)\
            .filter(Task.id == json_task['id']).first()
        task.new_file = f'{json_task["id"]}.{new_format}'
        task.estado = TaskStatus.PROCESSED
        db.session.add(task)
        db.session.commit()


@task_postrun.connect
def close_session(*args, **kwargs):
    print("CLOSE")
    # db.session.remove()