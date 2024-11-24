from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text

class GeracaoRepository:
    def __init__(self, db: SQLAlchemy):
        self.db = db
    
    def get_all(self, id_usina: int, start_date: str, end_date: str, group_by: str):
        try:
            # Construção da consulta inicial
            initial_query = f'SELECT '

            # Mapear os dados agrupados com agregação
            aggregation_mapper = {
                "mes": {
                    "select": "AVG(quantidade) AS total_quantidade, AVG(prognostico) AS total_prognostico, DATE_TRUNC('month', data)::date AS data",
                    "group_by": " GROUP BY DATE_TRUNC('month', data)"
                },
                "ano": {
                    "select": "AVG(quantidade) AS total_quantidade, AVG(prognostico) AS total_prognostico, DATE_TRUNC('year', data)::date AS data",
                    "group_by": " GROUP BY DATE_TRUNC('year', data)"
                },
            }

            if group_by and group_by in aggregation_mapper:
                initial_query += aggregation_mapper[group_by]["select"]
            else:
                initial_query += "id, quantidade, prognostico, data"

            # A consulta agora tem a estrutura correta: SELECT, FROM, WHERE
            initial_query += f" FROM geracao WHERE id_usina = {id_usina}"

            # Filtrando pelas datas
            if start_date:
                initial_query += f" AND data >= '{start_date}'"
            if end_date:
                initial_query += f" AND data <= '{end_date}'"

            # Agrupando os dados
            if group_by and group_by in aggregation_mapper:
                initial_query += aggregation_mapper[group_by]["group_by"]

            # Ordenando os resultados pela data
            query = text(initial_query + f' ORDER BY data')
            # Executando a consulta
            result = self.db.session.execute(query)
            return result.fetchall()
        except Exception as e:
            print(f"Erro ao buscar usinas: {e}")
            return None
