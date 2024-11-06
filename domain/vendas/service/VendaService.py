from domain.vendas.dto.VendaDTO import VendaDTO
from domain.vendas.exception import VendaInvalidaException, VendaNaoPermitidaException
from domain.produtos.model.Produto import Produto
from domain.clientes.model.Cliente import Cliente
from domain.vendas.model.Venda import Venda
from database.sessao import db

class VendaService:
    @staticmethod
    def realizar_venda(venda_dto: VendaDTO):
        # Validar se o cliente existe
        cliente = Cliente.query.get(venda_dto.cliente_id)
        if not cliente:
            raise VendaInvalidaException("Cliente inexistente.")

        # Validar se o produto existe e verificar o estoque
        produto = Produto.query.get(venda_dto.produto_id)
        if not produto:
            raise VendaInvalidaException("Produto inexistente.")
        
        # Verificar se a quantidade é válida
        if venda_dto.quantidade <= 0:
            raise VendaNaoPermitidaException("Quantidade de venda deve ser positiva.")
        
        # Realizar a venda
        venda = Venda(
            produto_id=venda_dto.produto_id,
            cliente_id=venda_dto.cliente_id,
            quantidade=venda_dto.quantidade,
            preco_total=venda_dto.preco_total
        )
        
        db.session.add(venda)
        db.session.commit()
        return venda
