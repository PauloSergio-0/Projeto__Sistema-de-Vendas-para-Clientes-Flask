from flask import request, jsonify
from domain.clientes.model import Cliente, Status
from database import db
from sqlalchemy.exc import IntegrityError

def register_routes_cliente(app):
    @app.route('/importar/cliente', methods=['POST'])
    def registro_clientes():
        try:
            data = request.get_json()
            status = data.get('status', Status.ATIVO.value).upper()
            cliente = Cliente(nome=data['nome'], endereco=data['endereco'], contato=data['contato'], status=status)

            db.session.add(cliente)
            db.session.commit()
            return jsonify({"mensagem": "Cliente importado com sucesso."}), 200

        except IntegrityError:
            db.session.rollback()
            return jsonify({"erro": "Email já cadastrado"}), 409

        except KeyError as e:
            return jsonify({"erro": f"Campo obrigatório ausente: {str(e)}"}), 400

        except Exception as e:
            return jsonify({"erro": str(e)}), 500

    @app.route('/cadastrar/cliente', methods=['POST'])
    def cadastrar_clientes():
        try:
            data = request.get_json()
            status = data.get('status', Status.ATIVO.value).upper()
            cliente = Cliente(nome=data['nome'], endereco=data['endereco'], contato=data['contato'], status=status)

            db.session.add(cliente)
            db.session.commit()
            return jsonify({"mensagem": "Cliente cadastrado com sucesso."}), 201

        except IntegrityError:
            db.session.rollback()
            return jsonify({"erro": "Email já cadastrado"}), 409

        except KeyError as e:
            return jsonify({"erro": f"Campo obrigatório ausente: {str(e)}"}), 400

        except Exception as e:
            return jsonify({"erro": str(e)}), 500

    @app.route('/listar/cliente', methods=['GET'])
    def get_clientes():
        try:
            clientes = Cliente.query.all()
            resultado = [
                {
                    'id': c.id,
                    'nome': c.nome,
                    'endereco': c.endereco,
                    'contato': c.contato,
                    'status': c.status.value
                } for c in clientes
            ]
            return jsonify({"resultado": resultado}), 200
        except Exception as e:
            return jsonify({"erro": str(e)}), 500

    @app.route('/listar/cliente/<int:id>', methods=['GET'])
    def get_cliente(id):
        try:
            cliente = Cliente.query.get_or_404(id)
            resultado = {
                'id': cliente.id,
                'nome': cliente.nome,
                'endereco': cliente.endereco,
                'contato': cliente.contato,
                'status': cliente.status.value
            }
            return jsonify({"resultado": resultado}), 200
        except Exception as e:
            return jsonify({"erro": str(e)}), 500

    @app.route('/atualizar/cliente/<int:id>', methods=['PUT'])
    def update_cliente(id):
        try:
            data = request.json
            cliente = Cliente.query.get_or_404(id)

            print("Status recebido:", data.get('status'))

            status = Status(data.get('status', cliente.status.value).upper())

            cliente.nome = data.get('nome', cliente.nome)
            cliente.endereco = data.get('endereco', cliente.endereco)
            cliente.contato = data.get('contato', cliente.contato)
            cliente.status = Status(status)
            db.session.commit()

            return jsonify({"mensagem": "Cliente atualizado com sucesso."}), 204

        except IntegrityError:
            db.session.rollback()
            return jsonify({"erro": "Email já cadastrado"}), 409

        except KeyError as e:
            return jsonify({"erro": f"Campo obrigatório ausente: {str(e)}"}), 400

        except Exception as e:
            return jsonify({"erro": str(e)}), 500

    @app.route('/inativar/cliente/<int:id>', methods=['PATCH'])
    def inativar_cliente(id):
        try:
            cliente = Cliente.query.get_or_404(id)
            if cliente.status == Status.INATIVO:
                return jsonify({"erro": "Cliente já está inativo."}), 400

            cliente.status = Status.INATIVO
            db.session.commit()

            return jsonify({"mensagem": "Cliente inativado com sucesso."}), 200

        except Exception as e:
            return jsonify({"erro": str(e)}), 500

    @app.route('/ativar/cliente/<int:id>', methods=['PATCH'])
    def ativar_cliente(id):
        try:
            cliente = Cliente.query.get_or_404(id)
            if cliente.status == Status.ATIVO:
                return jsonify({"erro": "Cliente já está ativo."}), 400

            cliente.status = Status.ATIVO
            db.session.commit()

            return jsonify({"mensagem": "Cliente ativado com sucesso."}), 200
        except Exception as e:
            return jsonify({"erro": str(e)}), 500

    @app.route('/excluir/cliente/<int:id>', methods=['DELETE'])
    def delete_cliente(id):
        try:
            cliente = Cliente.query.get_or_404(id)
            cliente.status = Status.DELETADO

            db.session.add(cliente)
            db.session.commit()

            return jsonify({"mensagem": "Cliente deletado com sucesso."}), 200
        except Exception as e:
            return jsonify({"erro": str(e)}), 500
