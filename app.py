from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_restful import Api
from build import create_app
from modelos import db
from vistas import VistaSingUp, VistaLogIn, VistaTasks, VistaSingleTask, VistaFiles


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
