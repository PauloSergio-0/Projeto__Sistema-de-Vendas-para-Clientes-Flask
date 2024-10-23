class ClienteUpdateDTO:
    def __init__(self, nome=None, endereco=None, email=None, status=None):
        self.nome = nome
        self.endereco = endereco
        self.email = email
        self.status = status

    def __repr__(self):
        return f"ClienteUpdateDTO(nome={self.nome}, endereco={self.endereco}, email={self.email}, status={self.status})"