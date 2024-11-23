# app/services.py
from app.db import db
from app.usina.repository import UsinaRepository

class UsinaService:
    def __init__(self):
        self.repository = UsinaRepository(db=db)

    def get_usinas(self, limit: int, offset: int):
        usinas = self.repository.get_all(limit=limit, offset=offset)
        if usinas:
            return {'usinas': [dict(id=u[0], potencia=u[1]) for u in usinas]}
        
        return {'message': 'Nenhuma usina encontrada'}