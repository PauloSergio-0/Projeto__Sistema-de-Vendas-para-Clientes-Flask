from flask import Blueprint, request, jsonify
from src.models import db, Cliente, Produto, Venda
from src.routes import routes_bp

# Criação do Blueprint principal para as rotas
routes_bp = Blueprint('routes_bp', __name__)

# Rotas para Clientes
@routes_bp.route('/clientes', methods=['GET'])
def listar_clientes():
    clientes = Cliente.query.all()
    return jsonify([{'id': cliente.id, 'nome': cliente.nome, 'endereco': cliente.endereco, 'contato': cliente.contato} for cliente in clientes])

@routes_bp.route('/clientes', methods=['POST'])
def adicionar_cliente():
    dados = request.get_json()
    novo_cliente = Cliente(nome=dados['nome'], endereco=dados['endereco'], contato=dados['contato'])
    db.session.add(novo_cliente)
    db.session.commit()
    return jsonify({"message": "Cliente adicionado com sucesso"}), 201

# Rotas para Produtos
@routes_bp.route('/produtos', methods=['GET'])
def listar_produtos():
    produtos = Produto.query.all()
    return jsonify([{'id': produto.id, 'nome': produto.nome, 'codigo': produto.codigo, 'categoria': produto.categoria, 'preco': produto.preco} for produto in produtos])

@routes_bp.route('/produtos', methods=['POST'])
def adicionar_produto():
    dados = request.get_json()
    novo_produto = Produto(nome=dados['nome'], codigo=dados['codigo'], categoria=dados['categoria'], preco=dados['preco'])
    db.session.add(novo_produto)
    db.session.commit()
    return jsonify({"message": "Produto adicionado com sucesso"}), 201

# Rotas para Vendas
@routes_bp.route('/vendas', methods=['GET'])
def listar_vendas():
    vendas = Venda.query.all()
    return jsonify([{'id_cliente': venda.id_cliente, 'id_produto': venda.id_produto, 'quantidade_vendida': venda.quantidade_vendida, 'data_da_venda': venda.data_da_venda} for venda in vendas])

@routes_bp.route('/vendas', methods=['POST'])
def registrar_venda():
    dados = request.get_json()
    nova_venda = Venda(id_cliente=dados['id_cliente'], id_produto=dados['id_produto'], quantidade_vendida=dados['quantidade_vendida'], data_da_venda=dados['data_da_venda'])
    db.session.add(nova_venda)
    db.session.commit()
    return jsonify({"message": "Venda registrada com sucesso"}), 201
