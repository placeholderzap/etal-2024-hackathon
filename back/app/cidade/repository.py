from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text

class CidadeRepository:
    def __init__(self, db: SQLAlchemy):
        self.db = db
    
    def get_details_from_cidade(self, id_cidade: int):
        try:
            query = text(f"SELECT * FROM mv_media_endereco WHERE id = {id_cidade};")
            result = self.db.session.execute(query)
            return result.fetchall()
        except Exception as e:
            print(f"Erro ao buscar detalhes da cidade: {e}")
            return None
   
   