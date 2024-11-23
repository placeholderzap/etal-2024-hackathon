from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text

class UsinaRepository:
    def __init__(self, db: SQLAlchemy):
        self.db = db
    
    def get_all(self, limit: int, offset: int):
        try:
            query = text(f'SELECT id, potencia FROM mv_usina LIMIT {limit} OFFSET {offset}')
            result = self.db.session.execute(query)
            return result.fetchall()
        except Exception as e:
            print(f"Erro ao buscar usinas: {e}")
            return None

   