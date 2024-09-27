import sqlite3 as conector

# Abertura de conexão e aquisição de cursor
conexao = conector.connect("sistema_vendas.db")
cursor = conexao.cursor()

# Criação da tabela Clientes
comando1 = '''
    CREATE TABLE IF NOT EXISTS Clientes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        endereco TEXT NOT NULL,
        contato INTEGER NOT NULL
    );'''

# Criação da tabela Produtos
comando2 = '''
    CREATE TABLE IF NOT EXISTS Produtos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        codigo INTEGER NOT NULL,
        categoria INTEGER NOT NULL,
        preco REAL NOT NULL
    );'''

# Criação da tabela Vendas
comando3 = '''
    CREATE TABLE IF NOT EXISTS Vendas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        id_cliente INTEGER NOT NULL,
        id_produto INTEGER NOT NULL,
        quantidade INTEGER NOT NULL,
        data_da_venda DATE NOT NULL,
        FOREIGN KEY(id_cliente) REFERENCES Clientes(id),
        FOREIGN KEY(id_produto) REFERENCES Produtos(id)
    );'''

# Executando os comandos
cursor.execute(comando1)
cursor.execute(comando2)
cursor.execute(comando3)

# Salvando as alterações no banco de dados
conexao.commit()

# Fechamento das conexões
cursor.close()
conexao.close()
