from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text

class GeracaoRepository:
    def __init__(self, db: SQLAlchemy):
        self.db = db
    
    def get_all(self, limit: int, offset: int, id_usina: int, start_date: str, end_date: str):
        try:
            initial_query = f'SELECT id, data, quantidade, prognostico FROM geracao WHERE id_usina = {id_usina}'
            if start_date:
                initial_query += f" AND data >= '{start_date}'"
            if end_date:
                initial_query += f" AND data <= '{end_date}'"
        
            query = text(initial_query + f' ORDER BY data LIMIT {limit} OFFSET {offset}')
            result = self.db.session.execute(query)
            return result.fetchall()
        except Exception as e:
            print(f"Erro ao buscar usinas: {e}")
            return None

   