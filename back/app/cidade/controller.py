# app/controllers.py
from app.cidade.service import CidadeService
from flask import Blueprint, jsonify, request

# Define o Blueprint
cidade_controller = Blueprint('cidade_controller', __name__)
cidade_service = CidadeService()

@cidade_controller.route('/cidades', methods=['GET'])
def get_all():
    limit = request.args.get('limit', 10, type=int)
    offset = request.args.get('offset', 0, type=int)
    search = request.args.get('search', None, type=str)
    region = request.args.get('region', None, type=str)
    result = cidade_service.get_all(limit=limit, offset=offset, search=search, region=region)
    return jsonify(result)

@cidade_controller.route('/cidades/<int:id_cidade>/usinas', methods=['GET'])
def usinas_from_cidade(id_cidade):
    result = cidade_service.usinas_from_cidade(id_cidade=id_cidade)
    return jsonify(result)

@cidade_controller.route('/cidades/<int:id_usina>/historico', methods=['GET'])
def get_historico_usina(id_usina):
    result = cidade_service.get_historico_usina(id_usina=id_usina)
    return jsonify(result)
