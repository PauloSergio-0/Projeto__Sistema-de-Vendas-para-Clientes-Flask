from datetime import datetime
from typing import List, Dict, Any, Union

from flask import jsonify

from database.sessao import db
from domain.vendas.model.Venda import Venda
from domain.vendas.exception.exception import VendaExisteException, ValidacaoException
from domain.produtos.exception.exception import ProdutoImportException
from domain.produtos.model.Produto import Produto
from domain.vendas.model.Status import Status


class VendaDTO:

    def listar_vendas(self) -> List[Dict[str, Union[str, Any]]]:
        vendas = Venda.query.all()

        resultado = [{
            'id': venda.id,
            'data': venda.data_venda.strftime('%d/%m/%Y'),
            'cliente_id': venda.cliente_id,
            'total': self.__tratar_valor(venda.preco_total),
            'status': self.get_descricao_status(venda.status)
        } for venda in vendas]

        return resultado

    def consultar_venda(self, id_venda: int) -> Dict[str, Union[str, Any]]:
        venda = Venda.query.get_or_404(id_venda)

        return {
            'id': venda.id,
            'data': venda.data_venda.strftime('%d/%m/%Y'),
            'cliente_id': venda.cliente_id,
            'total': self.__tratar_valor(venda.preco_total),
            'status': self.get_descricao_status(venda.status)
        }

    def cadastrar_venda(self, data: Dict[str, Any]) -> Dict[str, Union[str, Any]]:
        self.__validar_campos_obrigatorios(data)

        produto = Produto.query.get(data['produto_id'])
        if not produto:
            raise ValidacaoException("Produto inexistente")

        preco_total = produto.preco * int(data['quantidade'])

        venda = Venda(
            data['cliente_id'],
            data['produto_id'],
            data['quantidade'],
            data['data'],
            preco_total
        )

        db.session.add(venda)
        db.session.commit()

        return {
            'id': venda.id,
            'data': venda.data_venda.strftime('%d/%m/%Y'),
            'cliente_id': venda.cliente_id,
            'total': self.__tratar_valor(venda.preco_total),
            'status': self.get_descricao_status(venda.status)
        }

    def atualizar_venda(self, id_venda: int, data: Dict[str, Any]) -> Dict[str, Union[str, Any]]:
        self.__validar_campos_obrigatorios(data)

        venda = Venda.query.get_or_404(id_venda)
        venda.data = data.get('data', venda.data)
        venda.cliente_id = data.get('cliente_id', venda.cliente_id)
        venda.total = data.get('total', venda.total)
        
        status = data.get('status', venda.status)
        if status not in {Status.PENDENTE, Status.CONCLUIDA, Status.CANCELADA}:
            raise ValidacaoException("Status inválido. Deve ser 'pendente', 'concluida' ou 'cancelada'.")
        
        venda.status = status

        db.session.commit()

        return {
            'id': venda.id,
            'data': venda.data,
            'cliente_id': venda.cliente_id,
            'total': venda.total,
            'status': self.get_descricao_status(venda.status)
        }

    def get_descricao_status(self, status: str) -> str:
        if status == Status.PENDENTE:
            return "Pendente"
        elif status == Status.CONCLUIDA:
            return "Concluída"
        elif status == Status.CANCELADA:
            return "Cancelada"
        raise ValueError(f"Status inválido: {status}")

    def __validar_campos_obrigatorios(self, data: Dict[str, Any]) -> None:
        if 'data' not in data or not data['data']:
            raise ValidacaoException("O campo 'data' é obrigatório.")
        if 'cliente_id' not in data or not data['cliente_id']:
            raise ValidacaoException("O campo 'cliente_id' é obrigatório.")
        if 'produto_id' not in data or not data['produto_id']:
            raise ValidacaoException("O campo 'produtos' deve ser uma lista de produtos com pelo menos um item.")
        if 'quantidade' not in data or not data['quantidade'] or data['quantidade'] <= 0:
            raise ValidacaoException("O campo 'total' deve ser um número positivo.")

    def calcular_total_venda(self, produtos_ids: List[int]) -> float:
        total = 0.0
        for produto_id in produtos_ids:
            produto = Produto.query.get(produto_id)
            if produto:
                total += produto.preco
            else:
                raise ProdutoImportException(f"Produto com id {produto_id} não encontrado.")
        return total

    def __tratar_valor(self, valor: float) -> str:
        valor = f"R$ {'{:.2f}'.format(valor)}"
        valor = valor.replace('.', ',').replace('_', '.')
        return valor

    def __tratar_data(self, data) -> str:
        data_objeto = datetime.strptime(data, "%a, %d %b %Y %H:%M:%S %Z")
        data_formatada = data_objeto.strftime("%d/%m/%Y")

        return data_formatada
