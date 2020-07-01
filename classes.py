from peewee import *
from funcionalidades.seguranca import *
import os

arquivo = "teste.db"
db = SqliteDatabase(arquivo)

class BaseModel(Model):
    class Meta:
        database = db

class Local(BaseModel):
    cidade = CharField(primary_key=True)
    estado = CharField()
    regiao = CharField()

#Categoria -> Palavras Chaves
class Categoria(BaseModel):
    nome = CharField(primary_key=True)

class Prato(BaseModel):
    nome = CharField()
    preco = FloatField()
    descricao = CharField(null=True)
    ingredientes = CharField(null=True)
    #Dizer quando tal prato é ofertado no Restaurante
    #To pensando em criar um padrao de String para armazenar isso
    dia_periodo = CharField()
    categorias = ManyToManyField(Categoria)

class Bebida(BaseModel):
    nome = CharField()
    preco = FloatField()
    descricao = CharField() #Colocar info de ml, Litros etc...
    ingredientes = CharField(null=True)
    #Dizer quando tal prato é ofertado no Restaurante
    #To pensando em criar um padrao de String para armazenar isso
    dia_periodo = CharField()
    categorias = ManyToManyField(Categoria)

#Contem os Pratos e Bebidas de um Estabelecimento
class Cardapio(BaseModel):
    pratos = ManyToManyField(Prato)
    bebidas = ManyToManyField(Bebida)


#class Agenda(BaseModel):
#    vagas_livres = IntegerField()
#    total_reservas = Integer(Field)
#    regime = IntegerField()
#    modelo = CharField()

#class Data(BaseModel):
#    dia = DateTime()
#    horario_inicio = CharField()
#    horario_termino = CharField()
#    lotacao_maxima = IntegerField()
#    permitir_reserva = BooleanField(default=False)
#    agenda = ForeignKey(Agenda)
#    reservas = ManyToMany(Reserva)

class Cliente(BaseModel):
    cpf = CharField(primary_key=True, max_length=14)
    nome = CharField(max_length=100)
    idade = IntegerField()
    email = CharField()
    senha = CharField()
    #imagem = BlobField()
    telefone = CharField()
    #local?

#class Estabelecimento(BaseModel):
#    cnpj = CharField(primary_key=True, max_length=14)
#    nome_ficticio = CharField(max_length=100)
#    email = CharField()
#    senha = CharField()
    #imagem = BlobField()
#    telefone = CharField()
#    qtd_views = IntegerField()
#    local = ForeignKeyField(Local)
#    agenada = ForeignKeyField(Agenda)
#    cardapio = ForeignKeyField(Cardapio)

#class Reserva(BaseModel):
#    data_solicitacao = DateTimeField()
#    cliente = ForeignKeyField(Cliente)
#    qtd_pessoas = IntegerField()
#    duracao = IntegerField()
#    agenda = ForeignKeyField(Agenda)
#    confirmacao = BooleanField(default=False)

class Notificacao(BaseModel):
    pass

class Ranking(BaseModel):
    pass