class VendaInvalidaException(Exception):
    pass

class VendaNaoPermitidaException(Exception):
    pass

class ValidacaoException(Exception):
    def __init__(self, message="Erro de validação"):
        self.message = message
        super().__init__(self.message)

class VendaExisteException(Exception):
    def __init__(self, message="Venda já existe"):
        self.message = message
        super().__init__(self.message)

class VendaNaoEncontradaException(Exception):
    def __init__(self, message="Venda não encontrada"):
        self.message = message
        super().__init__(self.message)
