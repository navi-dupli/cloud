from flask import request
from flask_jwt_extended import create_access_token

from modelos import db, Usuario, UsuarioSchema
from flask_restful import Resource

usuario_schema = UsuarioSchema()


class VistaLogIn(Resource):
    def post(self):
        usuario = Usuario.query.filter(Usuario.username == request.form["username"],
                                       Usuario.password == request.form["password"]).first()
        db.session.commit()
        if usuario is None:
            return {"ok": False, "mensaje": "El usuario no existe"}, 404
        else:
            token_de_acceso = create_access_token(identity=usuario.id, additional_claims=usuario_schema.dump(usuario))
            return {"ok": True, "mensaje": "Inicio de sesión exitoso", "token": token_de_acceso}
