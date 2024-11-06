from typing import List, Dict, Any, Union
from database.sessao import db
from domain.vendas.model.Venda import Venda
from domain.vendas.exception.exception import VendaExisteException, ValidacaoException
from domain.produtos.model.Produto import Produto

class VendaDTO:
    """Classe de acesso aos dados de Venda."""

    def listar_vendas(self) -> List[Dict[str, Union[str, Any]]]:
        vendas = Venda.query.all()

        resultado = [{
            'id': venda.id,
            'data': venda.data,
            'cliente_id': venda.cliente_id,
            'total': venda.total,
            'status': self.get_descricao_status(venda.status),
            'status_code': venda.status
        } for venda in vendas]

        return resultado

    def consultar_venda(self, id_venda: int) -> Dict[str, Union[str, Any]]:
        venda = Venda.query.get_or_404(id_venda)

        return {
            'id': venda.id,
            'data': venda.data,
            'cliente_id': venda.cliente_id,
            'total': venda.total,
            'status': self.get_descricao_status(venda.status),
            'status_code': venda.status
        }

    def cadastrar_venda(self, data: Dict[str, Any]) -> Dict[str, Union[str, Any]]:
        self.__validar_campos_obrigatorios(data)

        venda = Venda(
            data['data'], 
            data['cliente_id'], 
            data['produtos'],  # Espera uma lista de produtos ou ids
            data['total'], 
            StatusVenda.PENDENTE  # Status inicial da venda
        )

        db.session.add(venda)
        db.session.commit()

        return {
            'id': venda.id,
            'data': venda.data,
            'cliente_id': venda.cliente_id,
            'total': venda.total,
            'status': self.get_descricao_status(venda.status)
        }

    def atualizar_venda(self, id_venda: int, data: Dict[str, Any]) -> Dict[str, Union[str, Any]]:
        self.__validar_campos_obrigatorios(data)

        venda = Venda.query.get_or_404(id_venda)
        venda.data = data.get('data', venda.data)
        venda.cliente_id = data.get('cliente_id', venda.cliente_id)
        venda.total = data.get('total', venda.total)

        # Atualiza status se fornecido
        status = data.get('status', venda.status)
        if status not in {StatusVenda.PENDENTE, StatusVenda.CONCLUIDA, StatusVenda.CANCELADA}:
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
        """Método para descrever o status da venda."""
        if status == StatusVenda.PENDENTE:
            return "Pendente"
        elif status == StatusVenda.CONCLUIDA:
            return "Concluída"
        elif status == StatusVenda.CANCELADA:
            return "Cancelada"
        raise ValueError(f"Status inválido: {status}")

    def __validar_campos_obrigatorios(self, data: Dict[str, Any]) -> None:
        """Valida os campos obrigatórios para criar ou atualizar uma venda."""
        if 'data' not in data or not data['data']:
            raise ValidacaoException("O campo 'data' é obrigatório.")
        if 'cliente_id' not in data or not data['cliente_id']:
            raise ValidacaoException("O campo 'cliente_id' é obrigatório.")
        if 'produtos' not in data or not isinstance(data['produtos'], list) or len(data['produtos']) == 0:
            raise ValidacaoException("O campo 'produtos' deve ser uma lista de produtos com pelo menos um item.")
        if 'total' not in data or not isinstance(data['total'], (int, float)) or data['total'] <= 0:
            raise ValidacaoException("O campo 'total' deve ser um número positivo.")

    def calcular_total_venda(self, produtos_ids: List[int]) -> float:
        """Calcula o total da venda com base nos produtos comprados."""
        total = 0.0
        for produto_id in produtos_ids:
            produto = Produto.query.get(produto_id)
            if produto:
                total += produto.preco
            else:
                raise ProdutoImportException(f"Produto com id {produto_id} não encontrado.")
        return total
