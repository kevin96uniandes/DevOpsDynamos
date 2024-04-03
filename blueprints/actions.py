from flask import jsonify, request, Blueprint
from ..service.blacklist_service import BlacklistService
from ..validators.validator import Validador
from flask_jwt_extended import jwt_required, create_access_token
from ..models.models import BlacklistSchema
import traceback

actions_blueprint = Blueprint('operations', __name__)
service = BlacklistService()
validador = Validador()
blacklist_schema = BlacklistSchema()

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

        validaciones = validador.validar_request_blacklist(data)
        if validaciones is not None:
            return jsonify({"msg": validaciones}), 400

        ip_address = request.remote_addr
        email_blacklist = service.crear_email_blacklist(data, ip_address)
        return blacklist_schema.dump(email_blacklist), 201
    except Exception as ex:
        traza_excepcion = traceback.format_exc()
        return jsonify({"msg": f"error a la hora de crear el registro {ex} {traza_excepcion}"}), 500

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