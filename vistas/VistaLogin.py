from flask import request
from flask_jwt_extended import create_access_token

from modelos import db, Usuario, UsuarioSchema, TaskSchema
from flask_restful import Resource

usuario_schema = UsuarioSchema()


class VistaLogIn(Resource):
    def post(self):
        return False
