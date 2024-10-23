"""from dataclasses import fields


class ClienteCreateDTO:
    def __init__(self, nome, endereco, email, status):
        self.nome = nome
        self.endereco = endereco
        self.email = email
        self.status = status

class ClienteCreateSchema(Schema):
    nome = fields.String(required=True, validate=validate.Length(min=1, max=50))
    endereco = fields.String(required=True, validate=validate.Length(min=1, max=100))
    email = fields.String(required=True, validate=validate.Email())
    status = fields.Boolean(required=False, missing=True)


def create_cliente(data):
    schema = ClienteCreateSchema()
    try:
        validated_data = schema.load(data)
        cliente_dto = ClienteCreateDTO(**validated_data)
        return cliente_dto
    except Exception as e:
        print(f"Erro: {e}")
        return None """
