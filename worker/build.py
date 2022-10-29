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
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = False
    app.config['JWT_SECRET_KEY'] = 'frase-secreta-para-cifrar-el-token'
    app.config['MAIL_SERVER'] = 'smtp.gmail.com'
    app.config['MAIL_PORT'] = 465
    app.config['MAIL_USERNAME'] = 'cloudteam35@gmail.com'
    app.config['MAIL_PASSWORD'] = 'uaeyqqzjlpvumqge'
    app.config['MAIL_USE_TLS'] = False
    app.config['MAIL_USE_SSL'] = True

    return app
