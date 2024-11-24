from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text

class CidadeRepository:
    def __init__(self, db: SQLAlchemy):
        self.db = db

    def get_total(self):
        try:
            query = text("SELECT COUNT(*) FROM cidade;")
            result = self.db.session.execute(query)
            return result.fetchone()[0]
        except Exception as e:
            print(f"Erro ao buscar total de cidades: {e}")
            return None

    def get_all(self, limit: int, offset: int, search: str):
        try:
            initial_query = f"""SELECT cidade.id, cidade.nome, estado.uf, estado.regiao
            FROM cidade
            JOIN estado ON cidade.id_estado = estado.id
            """
            if search:
                initial_query += f" WHERE cidade.nome ILIKE '%{search}%'"

            query = text(initial_query + f" LIMIT {limit} OFFSET {offset}")
            result = self.db.session.execute(query)
            return result.fetchall()
        except Exception as e:
            print(f"Erro ao buscar cidades: {e}")
            return None
    
    def get_details_from_cidade(self, id_cidade: int):
        try:
            query = text(f"SELECT * FROM mv_media_endereco WHERE id = {id_cidade};")
            result = self.db.session.execute(query)
            return result.fetchall()
        except Exception as e:
            print(f"Erro ao buscar detalhes da cidade: {e}")
            return None
   
   