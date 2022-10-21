import os

from celery import Celery
from celery.signals import task_postrun
from pydub import AudioSegment

from build import create_app
from env import REDIS_SERVER, REDIS_PORT, UPLOAD_FOLDER, CONVERTED_FOLDER
from modelos import db, Task, TaskStatus, Usuario
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
    if new_format == 'acc':
        convert_format = 'adts'
    given_audio = AudioSegment.from_file(os.path.join(UPLOAD_FOLDER, f'{json_task["id"]}.{format}'),
                                         format=format)
    given_audio.export(os.path.join(CONVERTED_FOLDER, f'{json_task["id"]}.{new_format}'), format=convert_format)

    print('entra a convertir', json_task['id'])
    return True


def send_mail(recipient, file_name):
    msg = Message('Conversión del archivo exitosa', sender='cloudteam35@gmail.com', recipients=[recipient])
    msg.body = f'El archivo {file_name} fue convertido exitosamente'
    mail.send(msg)
    return True




@celery_app.task(name="convertir-archivo")
def encolar(json_task):
    if convert_file(json_task):
        new_format = json_task['new_format'].lower()
        task = db.session.query(Task) \
            .filter(Task.id == json_task['id']).first()
        task.new_file = f'{json_task["id"]}.{new_format}'
        task.estado = TaskStatus.PROCESSED
        db.session.add(task)
        db.session.commit()
        usuario = Usuario.query.get(task.usuario)
        send_mail(usuario.correo, task.file)


@task_postrun.connect
def close_session(*args, **kwargs):
    print("CLOSE")
    # db.session.remove()
