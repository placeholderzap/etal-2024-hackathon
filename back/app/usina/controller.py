# app/controllers.py
from flask import Blueprint, jsonify, request
from app.geracao.service import GeracaoService
from app.usina.service import UsinaService

# Define o Blueprint
usina_controller = Blueprint('usina_controller', __name__)
usina_service = UsinaService()
geracao_service = GeracaoService()

@usina_controller.route('/usinas', methods=['GET'])
def get_usinas():
    search = request.args.get('search', None, type=str)
    limit = request.args.get('limit', 10, type=int)
    offset = request.args.get('offset', 0, type=int)
    result = usina_service.get_usinas(limit=limit, offset=offset, search=search)
    return jsonify(result)

@usina_controller.route('/usinas/<int:id>', methods=['GET'])
def get_usina(id):
    start_date = request.args.get('start_date', None, type=str)
    end_date = request.args.get('end_date', None, type=str)
    group_by = request.args.get('group_by', None, type=str)

    if group_by == 'dia':
        group_by = None

    result = geracao_service.get_geracao_by_usina_id(id_usina=id, group_by=group_by, start_date=start_date, end_date=end_date)
    return jsonify(result)

@usina_controller.route('/usinas/<int:id>/endereco', methods=['GET'])
def get_endereco_by_usina_id(id):
    result = usina_service.get_endereco_by_usina_id(id=id)
    return jsonify(result)
