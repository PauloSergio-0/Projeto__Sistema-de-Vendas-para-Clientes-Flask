from typing import List, Dict, Any
from src.database import db
from src.clientes.model import Cliente, Status
from src.clientes.exception import ClienteExisteException, ValidacaoException

class ClienteDTO:
    def get_descricao_status(self, status: str) -> str:
        if status == Status.ATIVO.value:
            return "Ativo"
        elif status == Status.INATIVO.value:
            return "Inativo"
        raise ValueError(f"Status inválido: {status}")

    def criar_cliente(self, data: Dict[str, Any]) -> Dict[str, Any]:
        self.validar_dados(data)

        if self.cliente_email(data['email']):
            raise ClienteExisteException("Já existe um cliente cadastrado com o email informado")

        cliente = Cliente(nome=data['nome'], endereco=data['endereco'], email=data['email'], status=Status.ATIVO)
        db.session.add(cliente)
        db.session.commit()

        return {
            'id': cliente.id,
            'nome': cliente.nome,
            'endereco': cliente.endereco,
            'email': cliente.email,
            'status': self.get_descricao_status(cliente.status.value)
        }

    def atualizar_cliente(self, id_cliente: int, data: Dict[str, Any]) -> Dict[str, Any]:
        self.validar_dados(data, is_update=True)

        cliente = Cliente.query.get_or_404(id_cliente)
        cliente.nome = data.get('nome', cliente.nome)
        cliente.endereco = data.get('endereco', cliente.endereco)
        cliente.email = data.get('email', cliente.email)

        status = data.get('status', cliente.status.value)
        if status not in {Status.ATIVO.value, Status.INATIVO.value}:
            raise ValidacaoException("Status deve ser 'ativo' ou 'inativo'.")

        cliente.status = Status(status.upper())

        db.session.commit()

        return {
            'id': cliente.id,
            'nome': cliente.nome,
            'endereco': cliente.endereco,
            'email': cliente.email,
            'status': self.get_descricao_status(cliente.status.value)
        }

    def listar_clientes(self) -> List[Dict[str, Any]]:
        clientes = Cliente.query.all()
        return [
            {
                'id': cliente.id,
                'nome': cliente.nome,
                'endereco': cliente.endereco,
                'email': cliente.email,
                'status': self.get_descricao_status(cliente.status.value)
            } for cliente in clientes
        ]

    def validar_dados(self, data: Dict[str, Any], is_update: bool = False) -> None:
        if 'nome' not in data or not data['nome'].strip():
            raise ValidacaoException("O campo 'nome' é obrigatório.")
        if 'endereco' not in data or not data['endereco'].strip():
            raise ValidacaoException("O campo 'endereco' é obrigatório.")
        if not is_update and ('email' not in data or not data['email'].strip()):
            raise ValidacaoException("O campo 'email' é obrigatório.")

    def cliente_email(self, email: str) -> bool:
        return Cliente.query.filter_by(email=email).first() is not None
