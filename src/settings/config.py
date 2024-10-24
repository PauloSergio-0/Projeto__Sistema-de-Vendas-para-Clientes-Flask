class Config:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///sistema_vendas.db'  
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    INATIVO = 0
    ATIVO = 1
    DELETADO = 2
