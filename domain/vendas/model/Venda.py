from datetime import date
from database.sessao import db
from sqlalchemy import Enum
from domain.vendas.model.Status import Status

class Venda(db.Model):
    __tablename__ = 'vendas'

    id = db.Column(db.Integer, primary_key=True)
    cliente_id = db.Column(db.Integer, nullable=False)
    produto_id = db.Column(db.Integer, nullable=False)
    quantidade = db.Column(db.Integer, nullable=False)
    data_venda = db.Column(db.Date, nullable=False)
    preco_total = db.Column(db.Float, nullable=False)
    status = db.Column(Enum(Status), default=Status.CONCLUIDA.value)

    def __init__(self, id_cliente: int, id_produto: int, quantidade: int, data_venda: date, preco_total: float):
        self.cliente_id = id_cliente
        self.produto_id = id_produto
        self.quantidade = quantidade
        self.data_venda = data_venda
        self.preco_total = preco_total
        self.status = Status.CONCLUIDA.value
