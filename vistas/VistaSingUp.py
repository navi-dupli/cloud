import re

from flask import request
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity

from modelos import Task ,db, Usuario, UsuarioSchema, TaskSchema
from flask_restful import Resource
from sqlalchemy import or_, desc, asc

usuario_schema = UsuarioSchema()
task_scheme = TaskSchema()


class VistaSingUp(Resource):
    def post(self):
        if request.json["password1"] != request.json["password2"]:
            return {"ok": False, "mensaje": "El password no coincide"}
        elif re.fullmatch(r'[A-Za-z0-9@#$%^&+=]{8,}', request.json["password1"]):
            return {"ok": False,
                    "mensaje": "El password no cumple con las condiciones minimas [8 caracteres alfanumericos] "}
        else:
            nuevo_usuario = Usuario(username=request.json["username"], password=request.json["password1"],
                                    correo=request.json["email"])

            usuario_existente_username = Usuario.query.filter(Usuario.username == nuevo_usuario.username).first()

            if usuario_existente_username:
                return {"ok": False, "mensaje": "El usuario debe ser unico"}
            else:
                usuario_existente_correo = Usuario.query.filter(Usuario.correo == nuevo_usuario.correo).first()
                if usuario_existente_correo:
                    return {"ok": False, "mensaje": "El correo electrónico debe ser unico"}
                else:
                    db.session.add(nuevo_usuario)
                    db.session.commit()
                    token_de_acceso = create_access_token(identity=nuevo_usuario.id,
                                                          additional_claims=usuario_schema.dump(nuevo_usuario))
                    return {"ok": True,
                            "mensaje": "usuario creado exitosamente",
                            "token": token_de_acceso,
                            "id": nuevo_usuario.id}





