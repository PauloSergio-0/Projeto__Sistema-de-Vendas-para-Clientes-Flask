from models import db


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

class Produto(db.Model):
    __tablename__ = 'produtos'

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(20), nullable=False)
    codigo = db.Column(db.Integer, nullable=False)
    categoria = db.Column(db.String(20), nullable=False)
    preco = db.Column(db.Float, nullable=False)

    def __init__(self, nome, codigo, categoria, preco):
        self.nome = nome 
        self.codigo = codigo
        self.categoria = categoria
        self.preco = preco 



class Venda(db.Model):
    __tablename__ = 'vendas'

    id = db.Column(db.Integer, primary_key=True)
    id_cliente = db.Column(db.Integer, db.Foreignkey('clientes.id'), nullable=False)
    id_produto = db.Column(db.Integer, db.Foreignkey('produtos.id'), nullable=False)
    quantidade_vendida = db.Column(db.Integer, nullable=False)
    data_da_venda = db.Column(db.Date, nullable=False)

    def __init__(self, id_cliente, id_produto, quantidade_vendida, data_da_venda):
        self.id_cliente = id_cliente
        self.id_produto = id_produto
        self.quantidade_vendida = quantidade_vendida
        self.data_da_venda = data_da_venda