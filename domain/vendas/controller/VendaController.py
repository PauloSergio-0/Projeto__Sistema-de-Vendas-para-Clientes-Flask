from flask import request, jsonify
from domain.vendas.dto.VendaDTO import VendaDTO
from domain.vendas.model import Venda
from database import db
from datetime import datetime
from sqlalchemy.exc import IntegrityError
from domain.vendas.exception.exception import VendaInvalidaException, VendaNaoPermitidaException, ValidacaoException, VendaNaoEncontradaException

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

    @app.route('/importar/venda', methods=['POST'])
    def importar_venda():
        try:
            # Recebe os dados da requisição JSON
            data = request.get_json()
            
            # Valida a presença dos campos obrigatórios no JSON
            # vendas = data.get("vendas")
            
            # if not vendas:
            #     return jsonify({"erro": "Nenhuma venda encontrada no payload"}), 400
            print(data)
            
            # Itera sobre as vendas no JSON

            # Obtendo os dados com os nomes exatos das colunas do CSV
            id_cliente = data.get("id_do_cliente")
            id_produto = data.get("id_do_produto")
            quantidade = data.get("quantidade")
            data_venda = data.get("data_da_venda")
            

            print("foi")
                # Verificação dos campos obrigatórios
            # if not all([id_cliente, id_produto, quantidade, data_venda]):
            #     return jsonify({"erro": "Campos obrigatórios ausentes em uma das vendas"}), 400

            # Converte a data para um objeto datetime, se necessário
            try:
                print("foi 2")
                data_venda = datetime.strptime(str(data_venda), "%Y-%m-%d")
            except ValueError:
                return jsonify({"erro": "Formato de data inválido. Use o formato YYYY-MM-DD"}), 400

            # Cria a instância de Venda
            venda = Venda(
                id_cliente=id_cliente,
                id_produto=id_produto,
                quantidade=quantidade,
                data_venda=data_venda
            )
            print("foi 3")

            # Adiciona a venda ao banco de dados
            db.session.add(venda)

            # Confirma as alterações no banco de dados
            db.session.commit()

            return jsonify({"mensagem": "Vendas importadas com sucesso!"}), 201

        except IntegrityError:
            # Lida com erros de integridade do banco de dados (por exemplo, IDs inexistentes)
            db.session.rollback()
            return jsonify({"erro": "Erro de integridade. Verifique os IDs fornecidos."}), 409

        except KeyError as e:
            # Campo obrigatório ausente
            return jsonify({"erro": f"Campo obrigatório ausente: {str(e)}"}), 400

        except Exception as e:
            # Erro genérico inesperado
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

    

    
