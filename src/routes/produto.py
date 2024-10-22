from http.client import HTTPException
from typing import Union

from flask import request, jsonify

from src.database.sessao import db
from src.exception.exception import ProdutoImportException, ProdutoExisteException
from src.models.produto import Produto, ProdutoDTO


def register_routes_produto(app):
	@app.route('/import_data/produto', methods=['POST'])
	def registro_produto():
		try:
			data = request.get_json()
			ProdutoDTO().importar_produto(data)

			return jsonify({
				"code": 201,
				"menssage": "adicionado com sucesso"
			}), 201
		except (ProdutoImportException, ProdutoExisteException) as e:
			return jsonify({
				"code": 406,
				"error": str(e)
			}), 406
		except Exception as e:
			return jsonify({
				"code": 500,
				"error": "Desculpe-me, ocorreu um erro inesperado."
			}), 500
