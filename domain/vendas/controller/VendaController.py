from flask import request, jsonify
from domain.vendas.dto.VendaDTO import VendaDTO
from domain.vendas.model.Venda import Venda
from domain.produtos.model.Produto import Produto
from database import db
from datetime import datetime
from sqlalchemy.exc import IntegrityError
from domain.vendas.exception.exception import ValidacaoException, VendaNaoEncontradaException

def register_routes_venda(app):
    @app.route('/listar/venda', methods=['GET'])
    def listar_vendas():
        try:
            vendas = VendaDTO().listar_vendas()
            return jsonify({
                "code": 200,
                "vendas": vendas
            }), 200
        except Exception as e:
            return jsonify({
                "code": 500,
                "error": "Desculpe-me, ocorreu um erro inesperado."
            }), 500

    @app.route('/listar/venda/<int:id>', methods=['GET'])
    def listar_venda(id):
        try:
            venda = VendaDTO().consultar_venda(id)
            return jsonify({
                "code": 200,
                "venda": venda
            }), 200
        except Exception as e:
            return jsonify({
                "code": 500,
                "error": "Desculpe-me, ocorreu um erro inesperado."
            }), 500

    @app.route('/listar/venda/cliente/<int:cliente_id>', methods=['GET'])
    def listar_vendas_cliente(cliente_id):
        try:
            vendas = VendaDTO().consultar_por_cliente_id(cliente_id)

            return jsonify({
                "code": 200,
                "venda": vendas
            }), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    @app.route('/listar/venda/produto/<int:produto_id>', methods=['GET'])
    def listar_vendas_produto(produto_id):
        try:
            vendas = VendaDTO().consultar_por_produto_id(produto_id)

            return jsonify({
                "code": 200,
                "venda": vendas
            }), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    @app.route('/listar/venda/data/<data>', methods=['GET'])
    def listar_vendas_data(data):
        try:
            data_venda = datetime.strptime(data, '%Y-%m-%d').date()
            vendas = VendaDTO().consultar_por_data_venda(data_venda)

            return jsonify({
                "code": 200,
                "venda": vendas
            }), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    @app.route('/importar/venda', methods=['POST'])
    def importar_venda():
        try:
            data = request.get_json()

            cliente_id = data.get("id_do_cliente")
            produto_id = data.get("id_do_produto")
            quantidade = data.get("quantidade")
            data_venda = data.get("data_da_venda")
            data_venda = datetime.strptime(data_venda, "%Y-%m-%d").date()

            produto = Produto.query.get(produto_id)
            if not produto:
                return jsonify({"erro": "Produto inexistente."}), 404

            preco_total = produto.preco * int(quantidade)

            venda = Venda(
                id_cliente=int(cliente_id),
                id_produto=int(produto.id),
                quantidade=int(quantidade),
                data_venda=data_venda,
                preco_total=preco_total
            )

            db.session.add(venda)
            db.session.commit()

            return jsonify({"mensagem": "Vendas importadas com sucesso!"}), 201
        except IntegrityError:
            db.session.rollback()
            return jsonify({"erro": "Erro de integridade. Verifique os IDs fornecidos."}), 409
        except KeyError as e:
            return jsonify({"erro": f"Campo obrigatório ausente: {str(e)}"}), 400
        except Exception as e:
            return jsonify({"erro": f"Desculpe, ocorreu um erro inesperado: {str(e)}"}), 500

    @app.route('/cadastrar/venda', methods=['POST'])
    def cadastrar_venda():
        try:
            data = request.get_json()
            venda = VendaDTO().cadastrar_venda(data)

            return jsonify({
                "code": 201,
                "msg": "Venda cadastrada com sucesso!",
                "venda": venda
            }), 201
        except (VendaNaoEncontradaException, ValidacaoException) as e:
            return jsonify({
                "code": 406,
                "error": str(e)
            }), 406
        except Exception as e:
                return jsonify({
                "code": 500,
                "error": "Desculpe-me, ocorreu um erro inesperado."
            }), 500

    @app.route('/atualizar/venda/<int:id>', methods=['PUT'])
    def atualizar_venda(id):
        try:
            data = request.get_json()
            venda = VendaDTO().atualizar_venda(id, data)

            return jsonify({
                "code": 201,
                "msg": "Venda atualizada com sucesso!",
                "venda": venda
            }), 201
        except (VendaNaoEncontradaException, ValidacaoException) as e:
            return jsonify({
                "code": 406,
                "error": str(e)
            }), 406
        except Exception as e:
            return jsonify({
                "code": 500,
                "error": f"Desculpe-me, ocorreu um erro inesperado. {str(e)}"
            }), 500

    @app.route('/cancelar/venda/<int:id>', methods=['DELETE'])
    def excluir_venda(id):
        try:
            VendaDTO().excluir_venda(id)

            return jsonify({
                "code": 200,
                "menssagem": "Venda cancelada com sucesso!"
            }), 200
        except Exception as e:
            return jsonify({
                "code": 500,
                "error": "Desculpe-me, ocorreu um erro inesperado."
            }), 500
