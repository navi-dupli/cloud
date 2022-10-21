from flask import Flask

from env import POSTGRES_USER, POSTGRES_PASSWORD, POSTGRES_URL, POSTGRES_DB


def create_app(config_name):
    app = Flask(__name__)
    DB_URL = 'postgresql://{user}:{pw}@{url}/{db}'.format(user=POSTGRES_USER, pw=POSTGRES_PASSWORD, url=POSTGRES_URL,
                                                          db=POSTGRES_DB)
    print(DB_URL)
    app.config['SQLALCHEMY_DATABASE_URI'] = DB_URL
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['PROPAGATE_EXCEPTIONS'] = True
    app.config['JWT_SECRET_KEY'] = 'frase-secreta-para-cifrar-el-token'

    return app
