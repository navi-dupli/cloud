from celery import Celery
from celery.signals import task_postrun
from env import REDIS_SERVER,REDIS_PORT

broker = f'redis://{REDIS_SERVER}:{REDIS_PORT}/0'



celery_app =Celery("WORKER", broker=broker)


@celery_app.task(name="convertir-archivo")
def encolar(id_task):
    pass



@task_postrun.connect()
def close_session(*args, **kwargs):
    print("CLOSE")
    # db.session.remove()
