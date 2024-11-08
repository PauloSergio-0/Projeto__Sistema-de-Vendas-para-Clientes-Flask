from flask import Flask

from database import db
from domain.clientes.controller.ClienteController import register_routes_cliente
from domain.produtos.controller.ProtudoController import register_routes_produto
from domain.vendas.controller.VendaController import register_routes_venda
from .config import Config

def create_app():
    
    app = Flask(__name__)
    
    app.config.from_object(Config)
    
    db.init_app(app)
    
    with app.app_context():
        db.create_all()
   
    register_routes_cliente(app)
    register_routes_produto(app)
    register_routes_venda(app)
    
    return app
