from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# Inicializando o aplicativo Flask
app = Flask(__name__)

# Configuração do banco de dados
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sistema_vendas.db'  
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Inicializando o SQLAlchemy
db = SQLAlchemy(app)

def init_db():
    with app.app_context():
        db.create_all()  # Cria as tabelas no banco de dados

# Executa a criação do banco de dados se este arquivo for executado diretamente
if __name__ == '__main__':
    init_db()
