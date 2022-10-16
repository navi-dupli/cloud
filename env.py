import os


def get_env_variable(name):
    try:
        return os.environ[name]
    except KeyError:
        message = "Expected environment variable '{}' not set.".format(name)
        raise Exception(message)


# the values of those depend on your setup


ALLOWED_EXTENSIONS = {'MP3', 'ACC', 'OGG', 'WAV', 'WMA'}
POSTGRES_URL = os.environ.get("POSTGRES_URL")
POSTGRES_USER = os.environ.get("POSTGRES_USER")
POSTGRES_PW = os.environ.get("POSTGRES_PW")
POSTGRES_DB = os.environ.get("POSTGRES_DB")
REDIS_SERVER = os.environ.get("REDIS_SERVER")
REDIS_PORT = os.environ.get("REDIS_PORT")
UPLOAD_FOLDER = os.environ.get("UPLOAD_FOLDER")
CONVERTED_FOLDER = os.environ.get("CONVERTED_FOLDER")
