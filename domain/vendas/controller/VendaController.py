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
            vendas = Venda.query.filter_by(cliente_id=cliente_id).all()

            vendas_json = [venda.to_dict() for venda in vendas]

            return jsonify(vendas_json), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    @app.route('/listar/venda/produto/<int:produto_id>', methods=['GET'])
    def listar_vendas_produto(produto_id):
        try:
            vendas = Venda.query.filter_by(produto_id=produto_id).all()

            vendas_json = [venda.to_dict() for venda in vendas]

            return jsonify(vendas_json), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    @app.route('/listar/venda/data', methods=['GET'])
    def listar_vendas_data():
        try:
            cliente_id = request.args.get('cliente_id', type=int)
            produto_id = request.args.get('produto_id', type=int)
            data_inicio = request.args.get('data_inicio')
            data_fim = request.args.get('data_fim')

            query = Venda.query

            if cliente_id:
                query = query.filter_by(cliente_id=cliente_id)
            if produto_id:
                query = query.filter_by(produto_id=produto_id)

            # data
            if data_inicio:
                try:
                    data_inicio = datetime.strptime(data_inicio, "%Y-%m-%d")
                except ValueError:
                    return jsonify({"error": "Formato inválido para data_inicio. Use YYYY-MM-DD."}), 400
                query = query.filter(Venda.data_venda >= data_inicio)

            if data_fim:
                try:
                    data_fim = datetime.strptime(data_fim, "%Y-%m-%d")
                except ValueError:
                    return jsonify({"error": "Formato inválido para data_fim. Use YYYY-MM-DD."}), 400
                query = query.filter(Venda.data_venda <= data_fim)

            vendas = query.all()
            vendas_json = [venda.to_dict() for venda in vendas]

            return jsonify({
                "code": 200,
                "vendas": vendas_json
            }), 200
        except Exception as e:
            return jsonify({
                "code": 500,
                "error": "Desculpe-me, ocorreu um erro inesperado."
            }), 500

    @app.route('/importar/venda', methods=['POST'])
    def importar_venda():
        try:
            data = request.get_json()

            id_cliente = data.get("id_do_cliente")
            id_produto = data.get("id_do_produto")
            quantidade = data.get("quantidade")
            data_venda = data.get("data_da_venda")
            data_venda = datetime.strptime(data_venda, "%Y-%m-%d").date()

            produto = Produto.query.get(id_produto)
            if not produto:
                return jsonify({"erro": "Produto inexistente."}), 404

            preco_total = produto.preco * int(quantidade)

            venda = Venda(
                id_cliente=int(id_cliente),
                id_produto=int(id_produto),
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

    @app.route('/atualizar/venda', methods=['PUT'])
    def atualizar_venda():
        try:
            data = request.get_json()
            venda = VendaDTO().atualizar_venda(data)
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

    @app.route('/ativar/venda', methods=["PATCH"])
    def ativar_venda():
        try:
            data = request.get_json()
            VendaDTO().ativar_venda(data['id'])  # Supondo que você tenha esse método na camada de serviço ou DTO

            return jsonify({
                "code": 200,
                "menssagem": "Venda ativada com sucesso!"
            }), 200
        except Exception as e:
            return jsonify({
                "code": 500,
                "error": "Desculpe-me, ocorreu um erro inesperado."
            }), 500

    @app.route('/inativar/venda', methods=["PATCH"])
    def inativar_venda():
        try:
            data = request.get_json()
            VendaDTO().inativar_venda(data['id'])

            return jsonify({
                "code": 200,
                "menssagem": "Venda inativada com sucesso!"
            }), 200
        except Exception as e:
            return jsonify({
                "code": 500,
                "error": "Desculpe-me, ocorreu um erro inesperado."
            }), 500

    @app.route('/excluir/venda', methods=['DELETE'])
    def excluir_venda():
        try:
            data = request.get_json()
            VendaDTO().excluir_venda(data['id'])
            return jsonify({
                "code": 200,
                "menssagem": "Venda deletada com sucesso!"
            }), 200
        except Exception as e:
            return jsonify({
                "code": 500,
                "error": "Desculpe-me, ocorreu um erro inesperado."
            }), 500
