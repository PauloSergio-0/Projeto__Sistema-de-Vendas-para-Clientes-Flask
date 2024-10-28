from flask import request, jsonify

def register_routes(app):
    @app.route('/import_data/cliente', methods=['POST'])
    def registro_clientes():
        # recebendo o json
        data = request.get_json()
        
        print(f"""
            id do cliente: {data['id']}
            nome do cliente: {data['nome']}
            endereço do cleinte: {data['endereco']}
            contato do cliente: {data['contato']}
            """)
    
        return jsonify({"menssage": "adcionado com sucesso"})
    
    @app.route('/import_data/venda', methods=['POST'])
    def registro_venda():
        data = request.get_json()
        
        print(f"""
            id do cliente: {data['id_do_cliente']}
            id do produto: {data['id_do_produto']}
            quantidade da venda: {data['quantidade']}
            data da venda: {data['data_da_venda']}
            """)
        
        return jsonify({"menssage": "adcionado com sucesso"})
