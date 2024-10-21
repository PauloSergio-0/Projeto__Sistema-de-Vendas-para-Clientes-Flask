from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# Inicializando o aplicativo Flask
app = Flask(__name__)

# Configuração do banco de dados
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sistema_vendas.db'  
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Inicializando o SQLAlchemy
db = SQLAlchemy(app)

# Função para criar as tabelas no banco de dados
def init_db():
    with app.app_context():
        db.create_all()  # Cria as tabelas no banco de dados

# Importando os modelos para garantir que eles sejam registrados com o SQLAlchemy
from src.models.models import Cliente, Produto, Venda
