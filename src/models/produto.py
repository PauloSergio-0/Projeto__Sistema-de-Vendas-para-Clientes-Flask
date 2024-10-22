from http.client import HTTPException

from src.database.sessao import db
from src.exception.exception import ProdutoImportException, ProdutoExisteException


class Produto(db.Model):
    __tablename__ = 'produtos'

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(50), nullable=False)
    codigo = db.Column(db.Integer, nullable=False)
    categoria = db.Column(db.String(30), nullable=False)
    preco = db.Column(db.Float, nullable=False)
    ativo = db.Column(db.Boolean, default=True, nullable=False)

    def __init__(self, nome: str, codigo: int, categoria: int, preco: float, ativo=True):
        self.id = None
        self.nome = nome
        self.codigo = codigo
        self.categoria = categoria
        self.preco = preco
        self.ativo = ativo


class ProdutoDTO:
    """Classe de acesso aos dados do Produto."""

    def importar_produto(self, data: dict) -> None:
        self.__validar_importacao_produto(data)

        produto = Produto(data['nome'], data['codigo'], data['categoria'], data['preco'])
        produto.id = data['id']

        db.session.add(produto)
        db.session.commit()

    def __validar_importacao_produto(self, data: dict) -> None:
        if 'id' not in data or not data['id']:
            raise ProdutoImportException("Para importar o produto é necessário ter o id do produto.")

        if self.__produto_existe(data['id']):
            raise ProdutoExisteException("Já existe um produto cadastrado para o id informado.")

    def __produto_existe(self, id_produto: int) -> bool:
        return Produto.query.filter_by(id=id_produto).first() is not None
