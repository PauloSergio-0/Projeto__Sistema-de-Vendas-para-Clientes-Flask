from flask import Flask

from src.database.sessao import db
from src.routes.routes_app import register_routes
from .config import Config
from ..produto.router.produto import register_routes_produto


def create_app():
    
    app = Flask(__name__)
    
    app.config.from_object(Config)
    
    db.init_app(app)
    
    with app.app_context():
        db.create_all()
   
    register_routes(app)
    register_routes_produto(app)
    
    return app
