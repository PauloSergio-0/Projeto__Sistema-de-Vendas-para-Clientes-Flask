from typing import List, Dict, Union, Any

from src.database.sessao import db
from src.exception.exception import ProdutoImportException, ProdutoExisteException, ValidacaoException
from src.produto.model.produto import Produto
from src.settings.config import Config


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
        if 'nome' not in data:
            raise ValidacaoException("Para importar o produto é necessário ter o nome do produto.")
        if not isinstance(data['nome'], str) or not data['nome'].strip():
            raise ValidacaoException("Para importar o produto o campo 'nome' deve ser uma string não vazia.")

        if 'codigo' not in data:
            raise ValidacaoException("Para importar o produto é necessário ter o código do produto.")
        if not isinstance(data['codigo'], int):
            raise ValidacaoException("Para importar o produto o campo 'codigo' deve ser um número inteiro.")

        if 'categoria' not in data:
            raise ValidacaoException("Para importar o produto é necessário ter a categoria do produto.")
        if not isinstance(data['categoria'], str) or not data['categoria'].strip():
            raise ValidacaoException("Para importar o produto o campo 'categoria' deve ser uma string não vazia.")

        if 'preco' not in data:
            raise ValidacaoException("Para importar o produto é necessário ter o preço do produto.")
        if not isinstance(data['preco'], (float, int)) or data['preco'] <= 0:
            raise ValidacaoException("Para importar o produto o campo 'preco' deve ser um número positivo.")

    def __existe_produto_com_id(self, id_produto: int) -> bool:
        return Produto.query.filter_by(id=id_produto).first() is not None

    def __existe_produto_com_codigo(self, codigo_produto: int, id_produto_ignorado: int = None) -> bool:
        query = Produto.query.filter_by(codigo=codigo_produto)

        if id_produto_ignorado:
            query = query.filter(Produto.id != id_produto_ignorado)

        return query.first() is not None

    def listar_produtos(self) -> List[Dict[str, Union[str, Any]]]:
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

    def cadastar_produto(self, data: dict) -> Dict[str, Union[str, Any]]:
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

    def inativar_produto(self, id_produto: int) -> None:
        produto = Produto.query.filter_by(id=id_produto).first()
        produto.status = Config.INATIVO

        db.session.add(produto)
        db.session.commit()

    def excluir_produto(self, id_produto: int) -> None:
        produto = Produto.query.filter_by(id=id_produto).first()
        produto.status = Config.DELETADO

        db.session.add(produto)
        db.session.commit()

    def atualizar_produto(self, data: dict) -> Dict[str, Union[str, Any]]:
        self.__validar_campos_obrigatorio(data)

        if self.__existe_produto_com_codigo(data['codigo'], data['id']):
            raise ProdutoExisteException("Já existe um produto cadastrado para o código informado.")

        produto = Produto.query.get_or_404(data['id'])
        produto.nome = data.get('nome', produto.nome)
        produto.codigo = data.get('codigo', produto.codigo)
        produto.categoria = data.get('categoria', produto.categoria)
        produto.preco = data.get('preco', produto.preco)

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
