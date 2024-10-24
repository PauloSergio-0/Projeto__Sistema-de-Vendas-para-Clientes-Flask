from src.database.sessao import db
from src.exception.exception import ProdutoImportException, ProdutoExisteException
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

class ProdutoDTO:
    """Classe de acesso aos dados do Produto."""

    def get_descricao_status(self, status: int) -> str:
        if status == Config.INATIVO:
            return "Inativo"

        if status == Config.ATIVO:
            return "Ativo"

        if status == Config.DELETADO:
            return "Deletado"

        raise ValueError(f"Status não configurado: {status}")

    def importar_produto(self, data: dict) -> None:
        self.__validar_importacao_produto(data)

        produto = Produto(data['nome'], data['codigo'], data['categoria'], data['preco'])
        produto.id = data['id']

        db.session.add(produto)
        db.session.commit()

    def __validar_importacao_produto(self, data: dict) -> None:
        if 'id' not in data or not data['id']:
            raise ProdutoImportException("Para importar o produto é necessário ter o id do produto.")

        self.__validar_campos_obrigatorio(data)

        if self.__existe_produto_com_id(data['id']):
            raise ProdutoExisteException("Já existe um produto cadastrado para o id informado.")

        if self.__existe_produto_com_codigo(data['codigo']):
            raise ProdutoExisteException("Já existe um produto cadastrado para o código informado.")

    def __validar_campos_obrigatorio(self, data: dict) -> None:
        if 'nome' not in data or not data['nome']:
            raise ProdutoImportException("Para importar o produto é necessário ter o nome do produto.")

        if 'codigo' not in data or not data['codigo']:
            raise ProdutoImportException("Para importar o produto é necessário ter o código do produto.")

        if 'categoria' not in data or not data['categoria']:
            raise ProdutoImportException("Para importar o produto é necessário ter a categoria do produto.")

        if 'preco' not in data or not data['preco']:
            raise ProdutoImportException("Para importar o produto é necessário ter o preço do produto.")

    def __existe_produto_com_id(self, id_produto: int) -> bool:
        return Produto.query.filter_by(id=id_produto).first() is not None

    def __existe_produto_com_codigo(self, codigo_produto: int) -> bool:
        return Produto.query.filter_by(codigo=codigo_produto).first() is not None

    def listar_produtos(self):
        produtos = Produto.query.all()

        resultado = [{
            'id': produto.id,
            'nome': produto.nome,
            'codigo': produto.codigo,
            'categoria': produto.categoria,
            'preco': produto.preco,
            'status': self.get_descricao_status(produto.status),
            'status_code': produto.status
        } for produto in produtos
        ]

        return resultado

    def cadastar_produto(self, data: dict):
        self.__validar_campos_obrigatorio(data)

        if self.__existe_produto_com_codigo(data['codigo']):
            raise ProdutoExisteException("Já existe um produto cadastrado para o código informado.")

        produto = Produto(data['nome'], data['codigo'], data['categoria'], data['preco'])

        db.session.add(produto)
        db.session.commit()

        return {
            'id': produto.id,
            'nome': produto.nome,
            'codigo': produto.codigo,
            'categoria': produto.categoria,
            'preco': produto.preco,
            'status': self.get_descricao_status(produto.status)
        }

    def inativar_produto(self, id_produto: int):
        produto = Produto.query.filter_by(id=id_produto).first()
        produto.status = Config.INATIVO

        db.session.add(produto)
        db.session.commit()

    def excluir_produto(self, id_produto: int):
        produto = Produto.query.filter_by(id=id_produto).first()
        produto.status = Config.DELETADO

        db.session.add(produto)
        db.session.commit()
