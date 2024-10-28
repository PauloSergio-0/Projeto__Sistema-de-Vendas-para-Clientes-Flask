from flask import request, jsonify

from src.exception.exception import ProdutoImportException, ProdutoExisteException, ValidacaoException
from src.produto.dto.produtoDTO import ProdutoDTO


def register_routes_produto(app):
	@app.route('/importar/produto', methods=['POST'])
	def importar_produto():
		try:
			data = request.get_json()
			ProdutoDTO().importar_produto(data)

			return jsonify({
				"code": 200,
				"menssagem": "Produto importado com sucesso!"
			}), 200
		except (ProdutoImportException, ProdutoExisteException, ValidacaoException) as e:
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
				"produto": produtos
			}), 200
		except Exception as e:
			return jsonify({
				"code": 500,
				"error": "Desculpe-me, ocorreu um erro inesperado."
			}), 500

	@app.route('/cadastrar/produto/', methods=['POST'])
	def cadastar_produto():
		try:
			data = request.get_json()
			produto = ProdutoDTO().cadastar_produto(data)

			return jsonify({
				"code": 201,
				"msg": "Produto cadastrado com sucesso!",
				"produto": produto
			}), 201
		except (ProdutoExisteException, ValidacaoException) as e:
			return jsonify({
				"code": 406,
				"error": str(e)
			}), 406
		except Exception as e:
			return jsonify({
				"code": 500,
				"error": "Desculpe-me, ocorreu um erro inesperado."
			}), 500

	@app.route('/atualizar/produto/', methods=['PUT'])
	def atualizar_produto():
		try:
			data = request.get_json()
			produto = ProdutoDTO().atualizar_produto(data)

			return jsonify({
				"code": 201,
				"msg": "Produto atualizado com sucesso!",
				"produto": produto
			}), 201
		except (ProdutoExisteException, ValidacaoException) as e:
			return jsonify({
				"code": 406,
				"error": str(e)
			}), 406
		except Exception as e:
			return jsonify({
				"code": 500,
				"error": f"Desculpe-me, ocorreu um erro inesperado."
			}), 500

	@app.route('/inativar/produto', methods=["PATCH"])
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

	@app.route('/excluir/produto/', methods=["DELETE"])
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