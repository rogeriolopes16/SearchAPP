class Cadastro:
    def __init__(self,  nome, email, tipo, empresa, responsavel):
        self.nome = nome
        self.email = email
        self.tipo = tipo
        self.empresa = empresa
        self.responsavel = responsavel


class Obj:
    def __init__(self,  tipo, descricao, responsavel):
        self.tipo = tipo
        self.descricao = descricao
        self.responsavel = responsavel