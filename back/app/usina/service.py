# app/services.py
from app.db import db
from app.usina.repository import UsinaRepository

class UsinaService:
    def __init__(self):
        self.repository = UsinaRepository(db=db)

    def get_usinas(self, limit: int, offset: int, search: str = None):
        usinas = self.repository.get_all(limit=limit, offset=offset, search=search)
        total = self.repository.get_total()
        if usinas:
            return {
                'count': total,
                'next': f'/usinas?limit={limit}&offset={offset+1}' if total > offset * limit else None,
                'previous': f'/usinas?limit={limit}&offset={offset-1}' if offset > 0 else None,
                'results': [dict(id=u[0], potencia=u[1]) for u in usinas]

            }
        
        return {'message': 'Nenhuma usina encontrada'}
    
    def get_endereco_by_usina_id(self, id: int):
        endereco = self.repository.get_address_by_id(id=id)
        if endereco:
            return {'cidade': endereco[0], 'uf': endereco[1], 'denominacao': endereco[2], 'regiao': endereco[3], 'cidade_id': endereco[4]}
        
        return {'message': 'Nenhum endereço encontrado'}