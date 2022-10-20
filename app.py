from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_restful import Api
from flask import Flask


from env import POSTGRES_USER, POSTGRES_PW, POSTGRES_URL, POSTGRES_DB
from modelos import db
from vistas import VistaSingUp, VistaLogIn, VistaTasks, VistaSingleTask, VistaFiles


def create_app(config_name):
    app = Flask(__name__)
    DB_URL = 'postgresql://{user}:{pw}@{url}/{db}'.format(user=POSTGRES_USER, pw=POSTGRES_PW, url=POSTGRES_URL,
                                                                      db=POSTGRES_DB)
    print(DB_URL)
    app.config['SQLALCHEMY_DATABASE_URI'] = DB_URL
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['PROPAGATE_EXCEPTIONS'] = True
    app.config['JWT_SECRET_KEY'] = 'frase-secreta-para-cifrar-el-token'
    app.config['MAIL_SERVER'] = 'smtp.gmail.com'
    app.config['MAIL_PORT'] = 465
    app.config['MAIL_USERNAME'] = 'cloudteam35@gmail.com'
    app.config['MAIL_PASSWORD'] = 'admincloud'
    app.config['MAIL_USE_TLS'] = False
    app.config['MAIL_USE_SSL'] = True

    return app


app = create_app('Cloud_Converter')

app_context = app.app_context()
app_context.push()

db.init_app(app)
db.create_all()

cors = CORS(app, resources={r'*': {"origins": "*"}})

api = Api(app)

jwtmanager = JWTManager(app)

api.add_resource(VistaSingUp, '/api/auth/signup')
api.add_resource(VistaLogIn, '/api/auth/login')
api.add_resource(VistaTasks, '/api/tasks')
api.add_resource(VistaSingleTask, '/api/tasks/<int:id_task>')
api.add_resource(VistaFiles, '/api/files/<filename>')


@app.after_request
def add_header(response):
    response.headers['Content-Type'] = 'application/json'
    return response
