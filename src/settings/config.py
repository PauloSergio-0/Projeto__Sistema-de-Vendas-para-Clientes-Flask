class Config:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///sistema_vendas.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False



    """ SQLALCHEMY_DATABASE_URI = 'sqlite:///sistema_vendas.db'   
    SQLALCHEMY_DATABASE_URI = 'mysql://root:123@localhost/sistema_vendas'"""

    """docker build -t sistema_vendas:latest .
    docker run -d --sistema_vendas mysqlC -p 3306:3306 -e MYSQL_ROOT_PASSWORD=123 -e MYSQL_DATABASE=sistema_vendas mysql:latest"""



