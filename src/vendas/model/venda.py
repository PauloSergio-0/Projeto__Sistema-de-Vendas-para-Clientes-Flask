from datetime import datetime, timezone


class Venda(db.Model):
    __tablename__ = 'vendas'

    id = db.Column(db.Integer, primary_key=True)
    cliente_id = db.Column(db.Integer, db.ForeignKey('clientes.id'), nullable=False)
    produto_id = db.Column(db.Integer, db.ForeignKey('produtos.id'), nullable=False)
    quantidade = db.Column(db.Integer, nullable=False)
    total = db.Column(db.Float, nullable=False)
    data_da_venda = db.Column(db.DateTime, default=datetime.now(timezone.utc))
    status = db.Column(db.Integer, default=Config.ATIVO)

    def __init__(self, cliente_id: int, produto_id: int, quantidade: int, total: float, data_da_venda=None):
        self.cliente_id = cliente_id
        self.produto_id = produto_id
        self.quantidade = quantidade
        self.total = total
        self.data_da_venda = data_da_venda if data_da_venda else datetime.now(timezone.utc)
        self.status = Config.ATIVO
