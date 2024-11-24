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


    def get_all(self, limit: int, offset: int, search: str):
        cidades = self.repository.get_all(limit=limit, offset=offset, search=search)
        total = self.repository.get_total()
        if cidades:
            return {
                'count': total,
                'next': f'/cidades?limit={limit}&offset={offset+1}' if total > offset * limit else None,
                'previous': f'/cidades?limit={limit}&offset={offset-1}' if offset > 0 else None,
                'results': [
                    dict(id=c[0], nome=c[1], uf=c[2], regiao=c[3])
                    for c in cidades
                ]
            }
        
        return {'message': 'Nenhuma cidade encontrada'}