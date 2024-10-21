from flask import Blueprint

# Cria um Blueprint para as rotas
routes_bp = Blueprint('routes', __name__)

# Importa as rotas do arquivo routes.py
from .routes import *
