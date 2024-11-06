from flask import request, jsonify
from domain.vendas.dto.VendaDTO import VendaDTO
from domain.vendas.exception.exception import VendaInvalidaException, VendaNaoPermitidaException, ValidacaoException

# Função para registrar as rotas de venda diretamente no app
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

    

    
