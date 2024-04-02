from flask import Flask, jsonify, request, Blueprint
from ..service.blacklist_service import BlacklistService

actions_blueprint = Blueprint('operations', __name__)
service = BlacklistService()

@actions_blueprint.route('/ping', methods = ['GET'])
def ping():
    return {"msg": "pong"}, 200 

@actions_blueprint.route('/', methods = ['POST'])
def crear_email():

    try:
        data = request.get_json()
        email_blacklist = service.crear_email_blacklist(data)
        return jsonify({"msg": f"el email {email_blacklist.email} con motivo de bloqueo {email_blacklist.blocked_reason} registro creado con exito"}), 201
    except Exception as ex:
        return jsonify({"msg": f"error a la hora de crear el registro {ex}"}), 500

@actions_blueprint.route('/<string:email>', methods = ['GET'])
def consultar_email(email):
    try:
        blacklist_item = service.consultar_by_email(email)
        if blacklist_item:
            return {"en lista negra": True, "blacklist item": blacklist_item}, 200
        else:
            return {"en lista negra": False}, 404
    except Exception as ex:
        return jsonify({"msg": f"error a la hora de consultar por el emmail {email} {ex}"}), 500