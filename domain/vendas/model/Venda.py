from datetime import datetime, timezone
from database.sessao import db
from settings.config import Config

class Venda(db.Model):
    __tablename__ = 'vendas'

    id = db.Column(db.Integer, primary_key=True)
    produto_id = db.Column(db.Integer, nullable=False)
    cliente_id = db.Column(db.Integer, nullable=False)
    quantidade = db.Column(db.Integer, nullable=False)
    data_venda = db.Column(db.DateTime, nullable=False)
    preco_total = db.Column(db.Float, nullable=False)

    def __init__(self, produto_id, cliente_id, quantidade, data_venda, preco_total):
        self.produto_id = produto_id
        self.cliente_id = cliente_id
        self.quantidade = quantidade
        self.preco_total = preco_total
        self.data_venda = data_venda
