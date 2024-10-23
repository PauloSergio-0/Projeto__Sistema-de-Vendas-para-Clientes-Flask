from src.database.sessao import db


class Cliente(db.Model):
    __tablename__ = 'clientes'

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(20), nullable=False)
    endereco = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(20), unique=True, nullable=False)
    status = db.Column(db.Boolean, default=True)

    def __init__(self, nome, endereco, contato, status):
        self.nome = nome
        self.endereco = endereco
        self.email = contato
        self.status = status