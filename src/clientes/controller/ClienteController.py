from flask import Flask, request, jsonify
from src.clientes.model import Cliente, Status
from src.database import db


def register_routes(app):
    @app.route('/cliente', methods=['POST'])
    def registro_clientes():
        try:
            data = request.get_json()
            status = data.get('status', Status.ATIVO.value)
            cliente = Cliente(nome=data['nome'], endereco=data['endereco'], email=data['email'], status=status)

            db.session.add(cliente)
            db.session.commit()
            return jsonify({"mensagem": "adicionado com sucesso", "id": cliente.id}), 201

        except Exception as e:
            return jsonify({"erro": str(e)}), 500

    @app.route('/cliente', methods=['GET'])
    def get_clientes():
        clientes = Cliente.query.all()
        resultado = [
            {
                'id': c.id,
                'nome': c.nome,
                'endereco': c.endereco,
                'email': c.email,
                'status': c.status.value
            } for c in clientes
        ]

        return jsonify({"resultado": resultado}), 200

    @app.route('/cliente/<int:id>', methods=['GET'])
    def get_cliente(id):
        cliente = Cliente.query.get_or_404(id)

        resultado = {
            'id': cliente.id,
            'nome': cliente.nome,
            'endereco': cliente.endereco,
            'email': cliente.email,
            'status': cliente.status.value
        }
        return jsonify({"resultado": resultado}), 200

    @app.route('/cliente/<int:id>', methods=['PUT'])
    def update_cliente(id):
        data = request.json
        cliente = Cliente.query.get_or_404(id)

        status = data.get('status', cliente.status.value)
        if status not in {Status.ATIVO.value, Status.INATIVO.value}:
            return jsonify({"erro": "Status deve ser 'ativo' ou 'inativo'"}), 400

        cliente.nome = data.get('nome', cliente.nome)
        cliente.endereco = data.get('endereco', cliente.endereco)
        cliente.email = data.get('email', cliente.email)
        cliente.status = Status(status)
        db.session.commit()

        return jsonify({'id': cliente.id}), 200

    @app.route('/cliente/<int:id>', methods=['DELETE'])
    def delete_cliente(id):
        cliente = Cliente.query.get_or_404(id)
        db.session.delete(cliente)
        db.session.commit()
        return jsonify({'mensagem': 'Cliente deletado'}), 204
