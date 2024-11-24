# app/services.py
from app.db import db
from app.cidade.repository import CidadeRepository

class CidadeService:
    def __init__(self):
        self.repository = CidadeRepository(db=db)
    
    def get_detalhes_cidade(self, id_cidade: int):
        detalhes_cidade = self.repository.get_details_from_cidade(id_cidade=id_cidade)
        if detalhes_cidade:
            return [
                dict(uf=d[0], id_cidade=d[1], regiao=d[2], denominacao=d[3], cidade=d[4], potencia=d[5], media_geracao=d[6], media_prognostico=d[7])
                for d in detalhes_cidade
            ]
        
        return {'message': 'Nenhum detalhe encontrado'}