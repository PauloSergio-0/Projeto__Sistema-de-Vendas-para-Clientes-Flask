from flask import Flask
from src.models import db, init_db
from src.routes import routes_bp

app = Flask(__name__)

# Configurações do banco de dados
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sistema_vendas.db'  
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Inicializando o banco de dados e o SQLAlchemy
db.init_app(app)

# Chama a função para criar o banco de dados dentro do contexto da aplicação
with app.app_context():
    init_db()  # Cria as tabelas no banco de dados

# Registrando as rotas com o Blueprint
app.register_blueprint(routes_bp)

if __name__ == '__main__':
    app.run(debug=True)
