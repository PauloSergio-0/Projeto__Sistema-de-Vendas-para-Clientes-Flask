from flask import Flask, request, jsonify


def register_routes(app):
    @app.route('/import_data/cliente', methods=['POST'])
    def registro_clientes():

        data = request.get_json()

        print(f"""
            id do cliente: {data['id']}
            nome do cliente: {data['nome']}
            endereço do cleinte: {data['endereco']}
            email do cliente: {data['email']}
            """)

        return jsonify({"menssage": "adcionado com sucesso"})
