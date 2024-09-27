class Cliente:
    def __init__(self, id, nome, endereco, contato):
        self.id = id
        self.nome = nome
        self.endereco = endereco
        self.contato = contato

class Produto:
    def __init__(self, id, nome, codigo, categoria, preco):
        self.id = id
        self.nome = nome
        self.codigo = codigo
        self.categoria = categoria
        self.preco = preco

class Venda:
    def __init__(self, id_cliente, id_produto, quantidade_vendida, data_da_venda):
        self.id_cliente = id_cliente
        self.id_produto = id_produto
        self.quantidade_vendida = quantidade_vendida
        self.data_da_venda = data_da_venda
