from flask import jsonify, request, Blueprint
from ..service.blacklist_service import BlacklistService
from flask_jwt_extended import jwt_required, create_access_token


actions_blueprint = Blueprint('operations', __name__)
service = BlacklistService()

@actions_blueprint.route('/ping', methods = ['GET'])
def ping():
    return {"msg": "pong"}, 200 

@actions_blueprint.route('/token', methods = ['GET'])
def generate_token():
    token = create_access_token(identity = 'DevOpsDynamos')
    return jsonify({"token": token})

@actions_blueprint.route('/', methods = ['POST'])
@jwt_required()
def crear_email():
    try:
        data = request.get_json()

        email = data.get('email')
        blacklist_item = service.consultar_by_email(email)
        if blacklist_item:
            return jsonify({"msg": f"el email {email} ya se encuentra registrado"}), 200

        email_blacklist = service.crear_email_blacklist(data)
        return jsonify({"msg": f"el email {email_blacklist.email} con motivo de bloqueo {email_blacklist.blocked_reason} registro creado con exito"}), 201
    except Exception as ex:
        return jsonify({"msg": f"error a la hora de crear el registro {ex}"}), 500

@actions_blueprint.route('/<string:email>', methods = ['GET'])
@jwt_required()
def consultar_email(email):
    try:
        blacklist_item = service.consultar_by_email(email)
        if blacklist_item:
            return {"en lista negra": True, "blacklist item": blacklist_item}, 200
        else:
            return {"en lista negra": False}, 404
    except Exception as ex:
        return jsonify({"msg": f"error a la hora de consultar por el emmail {email} {ex}"}), 500