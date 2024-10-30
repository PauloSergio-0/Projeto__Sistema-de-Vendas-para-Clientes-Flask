# src/vendas/dto/vendaDTO.py

from typing import List, Dict, Any
from datetime import datetime
from src.database.sessao import db
from src.produto.dto.produtoDTO import ProdutoDTO
from src.cliente.dto.clienteDTO import ClienteDTO
from src.vendas.model import Venda
from src.settings.config import Config


class VendaDTO:

    def get_descricao_status(self, status: int) -> str:
        if status == Config.INATIVO:
            return "Inativo"
        if status == Config.ATIVO:
            return "Ativo"
        if status == Config.DELETADO:
            return "Deletado"
        raise ValueError(f"Status inválido: {status}")

    def adicionar_venda(self, dados: Dict[str, Any]) -> Venda:
        """Adiciona uma nova venda ao banco de dados."""
        # Obtenha o produto e cliente usando os IDs fornecidos
        produto = ProdutoDTO().obter_produto(dados['id_do_produto'])
        cliente = ClienteDTO().obter_cliente(dados['id_do_cliente'])

        if not produto or not cliente:
            raise ValueError("Produto ou cliente não encontrado.")

        # Validações adicionais
        quantidade = dados.get('quantidade', 0)
        if quantidade <= 0:
            raise ValueError("A quantidade de vendas não pode ser negativa ou zero.")

        try:
            data_da_venda = datetime.strptime(dados['data_da_venda'], '%Y-%m-%d')
        except ValueError:
            raise ValueError("Data da venda deve estar no formato 'YYYY-MM-DD'.")

        total = produto.preco * quantidade  # Calcula o total da venda

        venda = Venda(
            cliente_id=cliente.id,
            produto_id=produto.id,
            quantidade=quantidade,
            total=total,
            data_da_venda=data_da_venda
        )

        db.session.add(venda)
        db.session.commit()
        return venda

    def listar_vendas(self, filtros: Dict[str, Any] = None) -> List[Dict[str, Any]]:
        """Lista todas as vendas, podendo aplicar filtros."""
        query = Venda.query

        if filtros:
            if 'cliente_id' in filtros:
                query = query.filter_by(cliente_id=filtros['cliente_id'])
            if 'produto_id' in filtros:
                query = query.filter_by(produto_id=filtros['produto_id'])
            if 'data_da_venda' in filtros:
                data = datetime.strptime(filtros['data_da_venda'], '%Y-%m-%d')
                query = query.filter_by(data_da_venda=data)

        vendas = query.all()

        # Criação do resultado de forma mais enxuta
        resultado = [{
            'id': venda.id,
            'cliente_id': venda.cliente_id,
            'produto_id': venda.produto_id,
            'quantidade': venda.quantidade,
            'total': venda.total,
            'data_da_venda': venda.data_da_venda,
            'status': self.get_descricao_status(venda.status),
            'status_code': venda.status
        } for venda in vendas]

        return resultado

    def atualizar_venda(self, venda_id: int, dados: Dict[str, Any]) -> Dict[str, Any]:
        """Atualiza uma venda existente com novos dados."""
        venda = Venda.query.get(venda_id)
        if not venda:
            raise ValueError("Venda não encontrada.")

        # Atualiza os campos da venda
        quantidade = dados.get('quantidade', venda.quantidade)
        if quantidade <= 0:
            raise ValueError("A quantidade de vendas não pode ser negativa ou zero.")

        venda.quantidade = quantidade
        venda.total = venda.produto.preco * quantidade  # Recalcula o total com o novo valor
        db.session.commit()

        return {
            'id': venda.id,
            'cliente_id': venda.cliente_id,
            'produto_id': venda.produto_id,
            'quantidade': venda.quantidade,
            'total': venda.total,
            'data_da_venda': venda.data_da_venda,
            'status': self.get_descricao_status(venda.status)
        }

    def inativar_venda(self, id_venda: int) -> None:
        venda = Venda.query.filter_by(id=id_venda).first()
        if not venda:
            raise ValueError("Venda não encontrada.")  # Lidar com o caso em que a venda não existe

        venda.status = Config.INATIVO  # Atualiza o status da venda para inativo

        db.session.add(venda)  # Adiciona a venda à sessão
        db.session.commit()  # Comita a transação

    def excluir_venda(self, venda_id):
        venda = Venda.query.get(venda_id)
        if not venda:
            raise ValueError("Venda não encontrada.")
        venda.status = Config.DELETADO
        db.session.commit()
