# app/services.py
from app.db import db
from app.cidade.repository import CidadeRepository
from datetime import datetime

class CidadeService:
    def __init__(self):
        self.repository = CidadeRepository(db=db)

    def get_historico_usina(self, id_usina: int):
        historico = self.repository.get_last_history(id_usina=id_usina)
        if historico:
            return [dict(id_cidade=h[0], usina_id=h[1], geracao=h[2], prognostico=h[3], data=datetime.strftime(h[4], '%Y-%m-%d'), estado_id=h[5], uf=h[6], regiao=h[7], potencia=h[8]) for h in historico]
        
        return []

    def usinas_from_cidade(self, id_cidade: int):
        usinas = self.repository.get_usinas_from_cidade(id_cidade=id_cidade)
        if usinas:
            return [dict(usina_id=u[0], uf=u[1], cidade_id=u[2], cidade=u[3], potencia=u[4]) for u in usinas]
        
        return []

    def get_all(self, limit: int, offset: int, search: str, region: str):
        cidades = self.repository.get_all(limit=limit, offset=offset, search=search, region=region)
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
        
        return {
            'count': 0,
            'next': None,
            'previous': None,
            'results': []
        }