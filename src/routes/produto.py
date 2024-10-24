from http.client import HTTPException
from typing import Union

from flask import request, jsonify

from src.database.sessao import db
from src.exception.exception import ProdutoImportException, ProdutoExisteException
from src.models.produto import Produto, ProdutoDTO


def register_routes_produto(app):
	@app.route('/import_data/produto', methods=['POST'])
	def importar_produto():
		try:
			data = request.get_json()
			ProdutoDTO().importar_produto(data)

			return jsonify({
				"code": 200,
				"menssagem": "Produto importado com sucesso"
			}), 200
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

	@app.route('/listar/produto', methods=['GET'])
	def listar_produtos():
		try:
			produtos = ProdutoDTO().listar_produtos()

			return jsonify({
				"code": 200,
				"produtos": produtos
			}), 200
		except Exception as e:
			return jsonify({
				"code": 500,
				"error": f"Desculpe-me, ocorreu um erro inesperado. {str(e)}"
			}), 500

	@app.route('/cadastrar/produto/', methods=['POST'])
	def cadastar_produto():
		try:
			data = request.get_json()
			produto = ProdutoDTO().cadastar_produto(data)

			return jsonify({
				"code": 201,
				"produto": produto
			}), 201
		except ProdutoExisteException as e:
			return jsonify({
				"code": 406,
				"error": str(e)
			}), 406
		except Exception as e:
			return jsonify({
				"code": 500,
				"error": "Desculpe-me, ocorreu um erro inesperado."
			}), 500

	@app.route('/inativar/produto', methods=["POST"])
	def inativar_produto():
		try:
			data = request.get_json()
			ProdutoDTO().inativar_produto(data['id'])

			return jsonify({
				"code": 200,
				"menssagem": "Produto inativado com sucesso!"
			}), 200
		except Exception as e:
			return jsonify({
				"code": 500,
				"error": "Desculpe-me, ocorreu um erro inesperado."
			}), 500

	@app.route('/excluir/produto/', methods=["POST"])
	def excluir_produto():
		try:
			data = request.get_json()
			ProdutoDTO().excluir_produto(data['id'])

			return jsonify({
				"code": 200,
				"menssagem": "Produto deletado com sucesso!"
			}), 200
		except Exception as e:
			return jsonify({
				"code": 500,
				"error": "Desculpe-me, ocorreu um erro inesperado."
			}), 500
