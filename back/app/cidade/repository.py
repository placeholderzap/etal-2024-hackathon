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

    def get_all(self, limit: int, offset: int, search: str, region: str):
        try:
            initial_query = f"""SELECT cidade.id, cidade.nome, estado.uf, estado.regiao
            FROM cidade
            JOIN estado ON cidade.id_estado = estado.id
            """
            if search:
                initial_query += f" WHERE cidade.nome ILIKE '%{search}%'"

            if region:
                initial_query += f" WHERE estado.regiao ILIKE '%{region}%'"

            query = text(initial_query + f" LIMIT {limit} OFFSET {offset}")
            result = self.db.session.execute(query)
            return result.fetchall()
        except Exception as e:
            print(f"Erro ao buscar cidades: {e}")
            return None
        
    def get_usinas_from_cidade(self, id_cidade: int, limit: int):
        try:
            query = text(f""" SELECT 
                                u.id as usina_id,
                                es.uf,
                                c.id as cidade_id,
                                c.nome AS cidade,
                                u.potencia
                            FROM unidade_consumidora uc
                                JOIN endereco e ON e.id::double precision = uc.id_endereco
                                JOIN cidade c ON c.id::double precision = e.id_cidade
                                JOIN estado es ON es.id = c.id_estado
                                JOIN usina u ON u.unidade_consumidora_id = uc.id
                            WHERE c.id = {id_cidade}
                            LIMIT {limit};""")
            result = self.db.session.execute(query)
            return result.fetchall()
        except Exception as e:
            print(f"Erro ao buscar usinas: {e}")
   
    def get_last_history(self, id_usina: int):
        try:
            query = text(f"""SELECT cidade.id as cidade_id, usina.id as usina_id, geracao.quantidade, geracao.prognostico, geracao.data::date, estado.id as estado_id, estado.uf, estado.regiao, usina.potencia as potencia
                            FROM usina
                            JOIN unidade_consumidora as uc ON uc.id = usina.unidade_consumidora_id
                            JOIN endereco ON uc.id_endereco = endereco.id
                            JOIN cidade ON endereco.id_cidade = cidade.id
                            JOIN estado ON estado.id = cidade.id_estado
                            JOIN geracao ON usina.id = geracao.id_usina
                            WHERE usina.id = {id_usina}
                            LIMIT 2000;""")
            result = self.db.session.execute(query)
            return result.fetchall()
        except Exception as e:
            print(f"Erro ao buscar historico: {e}")
            return None