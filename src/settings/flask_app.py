from flask import Flask

from src.database import db
from src.clientes.controller.ClienteController import register_routes_cliente
from .config import Config
from ..produto.controller.produto import register_routes_produto


def create_app():
    
    app = Flask(__name__)
    
    app.config.from_object(Config)
    
    db.init_app(app)
    
    with app.app_context():
        db.create_all()
   
    register_routes_cliente(app)
    register_routes_produto(app)
    
    return app
