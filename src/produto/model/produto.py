from src.database.sessao import db
from src.settings.config import Config

class Produto(db.Model):
    __tablename__ = 'produtos'

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(50), nullable=False)
    codigo = db.Column(db.Integer, nullable=False)
    categoria = db.Column(db.String(30), nullable=False)
    preco = db.Column(db.Float, nullable=False)
    status = db.Column(db.Integer, default=True, nullable=False)

    def __init__(self, nome: str, codigo: int, categoria: str, preco: float, status=Config.ATIVO):
        self.id = None
        self.nome = nome
        self.codigo = codigo
        self.categoria = categoria
        self.preco = preco
        self.status = status
