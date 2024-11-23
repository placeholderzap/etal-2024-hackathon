from app.db import db
from app.geracao.repository import GeracaoRepository

class GeracaoService:
    def __init__(self):
        self.repository = GeracaoRepository(db=db)

    def __get_geracao_saude(self, geracao: float, prognostico: float):
        if geracao > prognostico * 1.2:
            return 'erro_cadastro'
        elif geracao < prognostico * 0.7:
            return 'erro_medicao'
        
        return 'ok'

    def get_geracao_by_usina_id(self, group_by: str, id_usina: int, start_date: str, end_date: str):
        geracao_usina = self.repository.get_all(id_usina=id_usina, group_by=group_by, start_date=start_date, end_date=end_date)
        if geracao_usina and not group_by:
            return {'geracao': [dict(id=g[0], data=g[3], quantidade=g[1], prognostico=g[2], saude=self.__get_geracao_saude(geracao=g[1], prognostico=g[2])) for g in geracao_usina]}
        elif geracao_usina and group_by:
            return {'geracao': [dict(data=g[2], quantidade=g[0], prognostico=g[1], saude=self.__get_geracao_saude(geracao=g[0], prognostico=g[1])) for g in geracao_usina]}
        
        return {'message': 'Nenhuma usina encontrada'}