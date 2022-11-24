import os


def get_env_variable(name):
    try:
        return os.environ[name]
    except KeyError:
        message = "Expected environment variable '{}' not set.".format(name)
        raise Exception(message)


# the values of those depend on your setup


ALLOWED_EXTENSIONS = {'MP3', 'AAC', 'OGG', 'WAV', 'WMA'}
POSTGRES_URL = os.environ.get("POSTGRES_URL")
POSTGRES_USER = os.environ.get("POSTGRES_USER")
POSTGRES_PASSWORD = os.environ.get("POSTGRES_PASSWORD")
POSTGRES_DB = os.environ.get("POSTGRES_DB")
REDIS_SERVER = os.environ.get("REDIS_SERVER")
REDIS_PORT = os.environ.get("REDIS_PORT")
UPLOAD_FOLDER = os.environ.get("UPLOAD_FOLDER")
CONVERTED_FOLDER = os.environ.get("CONVERTED_FOLDER")
MAIL_NOTIFICATION_ENABLED = os.environ.get("MAIL_NOTIFICATION_ENABLED")
BUCKET_NAME = os.environ.get("BUCKET_NAME")
PROJECT_ID = os.environ.get("PROJECT_ID")
SUBSCRIBER = os.environ.get("SUBSCRIBER")
