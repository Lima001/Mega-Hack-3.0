from peewee import *

arquivo = "teste.db"
db = SqliteDatabase(arquivo)

class BaseModel(Model):
    class Meta:
        database = db

class Cliente(Model):
    cpf = CharField(primary_key=True, max_length=14)
    nome = CharField(max_length=100)
    idade = IntegerField
    email = CharField()
    senha = CharField()
    imagem = BlobField()
    telefone = CharField()
    #local?

class Estabelecimento(Model):
    cnpj = CharField(primary_key=True, max_length=14)
    nome_ficticio = CharField(max_length=100)
    email = CharField()
    senha = CharField()
    imagem = BlobField()
    telefone = CharField()
    local = ForeignKeyField(Local)
    agenada = ForeignKeyField(Agenda)
    cardapio = ForeignKeyField(Cardapio)

#Classe para representar os horários de atendimento, reservas já feitas,
#Qtd máxima de pessoas etc...
class Agenda(Model):
    pass

#Contem os Pratos e Bebidas de um Estabelecimento
class Cardapio(Model):
    pass

class Prato(Model):
    pass

class Bebida(Model):
    pass

class Reserva(Model):
    data = DateTimeField()
    cliente = ForeignKeyField(Cliente)
    agenda = ForeignKeyField(Agenda)
    confirmacao = BooleanField(default=False)

class Notificacao(Model):
    pass

class Ranking(Model):
    pass

class Local(Model):
    cidade = CharField(primary_key=True)
    estado = CharField()