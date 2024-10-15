from database import db


class Cliente(db.Model):
    __tablename__ = 'clientes'

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(20), nullable=False)
    endereco = db.Column(db.String(50), nullable=False)  
    contato = db.Column(db.String(15), nullable=False) 

    def __init__(self, nome, endereco, contato):
        self.nome = nome
        self.endereco = endereco
        self.contato = contato
