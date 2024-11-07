from datetime import datetime, timezone
from database.sessao import db
from settings.config import Config

class Venda(db.Model):
    __tablename__ = 'vendas'

    id = db.Column(db.Integer, primary_key=True)
    cliente_id = db.Column(db.Integer, nullable=False)
    produto_id = db.Column(db.Integer, nullable=False)
    quantidade = db.Column(db.Integer, nullable=False)
    data_venda = db.Column(db.Date, nullable=False)
    preco_total = db.Column(db.Float, nullable=False)

    def __init__(self, id_cliente: int, id_produto: int, quantidade: int, data_venda: datetime, preco_total: float):
        self.cliente_id = id_cliente
        self.produto_id = id_produto
        self.quantidade = quantidade
        self.data_venda = data_venda
        self.preco_total = preco_total
