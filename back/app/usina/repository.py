from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text

class UsinaRepository:
    def __init__(self, db: SQLAlchemy):
        self.db = db


    def get_address_by_id(self, id: int):
        try:
            query = text(f"""SELECT cidade.nome, estado.uf, estado.denominacao, estado.regiao, cidade.id
            FROM usina 
            JOIN unidade_consumidora ON unidade_consumidora.id = usina.unidade_consumidora_id 
            JOIN endereco ON unidade_consumidora.id_endereco = endereco.id
            JOIN cidade ON endereco.id_cidade = cidade.id
            JOIN estado ON cidade.id_estado = estado.id
            WHERE usina.id = {id};""")
            result = self.db.session.execute(query)
            return result.fetchone()
        except Exception as e:
            print(f"Erro ao buscar usina: {e}")
            return None
    
    def get_all(self, limit: int, offset: int, search: str = None):
        try:
            initial_query = 'SELECT id, potencia FROM mv_usina'
            if search:
                initial_query += f" WHERE CAST(id AS TEXT) LIKE '%{search}%'"
            
            query = text(f'{initial_query} LIMIT {limit} OFFSET {offset}')
            result = self.db.session.execute(query)
            return result.fetchall()
        except Exception as e:
            print(f"Erro ao buscar usinas: {e}")
            return None

    def get_total(self):
        try:
            query = text('SELECT COUNT(*) FROM mv_usina')
            result = self.db.session.execute(query)
            return result.fetchone()[0]
        except Exception as e:
            print(f"Erro ao buscar total de usinas: {e}")
            return None

   