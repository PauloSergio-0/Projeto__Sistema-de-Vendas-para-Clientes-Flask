# src/vendas/router/venda.py

from flask import request, jsonify
from src.vendas.dto.vendaDTO import VendaDTO

def register_routes_venda(app):
    @app.route('/importar/venda', methods=['POST'])
    def importar_venda():
        try:
            dados = request.get_json()
            vendas_importadas = VendaDTO().importar_vendas(dados)

            return jsonify({
                "code": 200,
                "mensagem": f"{len(vendas_importadas)} vendas importadas com sucesso!"
            }), 200
        except Exception as e:
            return jsonify({"code": 500, "error": "Erro inesperado."}), 500

    @app.route('/vendas', methods=['GET'])
    def listar_vendas():
        filtros = request.args.to_dict()
        vendas = VendaDTO().listar_vendas(filtros)
        vendas_json = [{
            "id": venda.id,
            "cliente_id": venda.cliente_id,
            "produto_id": venda.produto_id,
            "quantidade": venda.quantidade,
            "total": venda.total,
            "data_da_venda": venda.data_da_venda.strftime('%Y-%m-%d')
        } for venda in vendas]

        return jsonify({"code": 200, "vendas": vendas_json}), 200

    @app.route('cadastrar/vendas', methods=['POST'])
    def registrar_venda():
        try:
            dados = request.get_json()
            venda = VendaDTO().adicionar_venda(dados)
            return jsonify({
                "code": 201,
                "mensagem": "Venda registrada com sucesso!",
                "venda": {
                    "id": venda.id,
                    "cliente_id": venda.cliente_id,
                    "produto_id": venda.produto_id,
                    "quantidade": venda.quantidade,
                    "total": venda.total,
                    "data_da_venda": venda.data_da_venda.strftime('%Y-%m-%d')
                }
            }), 201
        except ValueError as e:
            return jsonify({"code": 400, "error": str(e)}), 400
        except Exception as e:
            return jsonify({"code": 500, "error": "Erro inesperado."}), 500

    @app.route('/atualizar/venda/', methods=['PUT'])
    def atualizar_venda():
        try:
            dados = request.get_json()
            venda = VendaDTO().atualizar_venda(dados)

            return jsonify({
                "code": 200,
                "mensagem": "Venda atualizada com sucesso!",
                "venda": {
                    "id": venda.id,
                    "cliente_id": venda.cliente_id,
                    "produto_id": venda.produto_id,
                    "quantidade": venda.quantidade,
                    "total": venda.total,
                    "data_da_venda": venda.data_da_venda.strftime('%Y-%m-%d')
                }
            }), 200
        except ValueError as e:
            return jsonify({"code": 400, "error": str(e)}), 400
        except Exception as e:
            return jsonify({"code": 500, "error": "Erro inesperado."}), 500

    @app.route('/inativar/venda/', methods=['PATCH'])
    def inativar_venda():
        try:
            dados = request.get_json()
            VendaDTO().inativar_venda(dados['id'])

            return jsonify({
                "code": 200,
                "mensagem": "Venda inativada com sucesso!"
            }), 200
        except ValueError as e:
            return jsonify({"code": 400, "error": str(e)}), 400
        except Exception as e:
            return jsonify({"code": 500, "error": "Erro inesperado."}), 500

    @app.route('/excluir/venda/<int:venda_id>', methods=['DELETE'])
    def excluir_venda(venda_id):
        try:
            VendaDTO().excluir_venda(venda_id)
            return jsonify({"code": 200, "mensagem": "Venda excluída logicamente com sucesso!"}), 200
        except ValueError as e:
            return jsonify({"code": 400, "error": str(e)}), 400
        except Exception as e:
            return jsonify({"code": 500, "error": "Erro inesperado."}), 500
