from app.db import db
from app.geracao.repository import GeracaoRepository

class GeracaoService:
    def __init__(self):
        self.repository = GeracaoRepository(db=db)

    def get_geracao_by_usina_id(self, limit: int, offset: int, id_usina: int, start_date: str, end_date: str):
        geracao_usina = self.repository.get_all(limit=limit, offset=offset, id_usina=id_usina, start_date=start_date, end_date=end_date)
        if geracao_usina:
            return {'geracao': [dict(id=g[0], data=g[1], quantidade=g[2], prognostico=g[3]) for g in geracao_usina]}
        
        return {'message': 'Nenhuma usina encontrada'}