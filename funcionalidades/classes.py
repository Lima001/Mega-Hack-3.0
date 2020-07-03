from peewee import *
import os

arquivo = "teste.db"
db = SqliteDatabase(arquivo)

class BaseModel(Model):
    class Meta:
        database = db

class Local(BaseModel):
    cidade = CharField()
    estado = CharField()
    regiao = CharField()

#Categoria -> Palavras Chaves
class Categoria(BaseModel):
    nome = CharField(primary_key=True)

class Prato(BaseModel):
    nome = CharField()
    preco = FloatField()
    imagem = BlobField(null=True)
    descricao = CharField(null=True)
    ingredientes = CharField(null=True)
    #Dizer quando tal prato é ofertado no Restaurante
    #To pensando em criar um padrao de String para armazenar isso
    dia_periodo = CharField()
    avaliacao = FloatField(null=True)
    categorias = ManyToManyField(Categoria)

class Bebida(BaseModel):
    nome = CharField()
    preco = FloatField()
    imagem = BlobField(null=True)
    descricao = CharField(null=True)
    ingredientes = CharField(null=True)
    #Dizer quando tal bebida é ofertado no Restaurante
    #To pensando em criar um padrao de String para armazenar isso
    dia_periodo = CharField()
    nota = FloatField(null=True)
    categorias = ManyToManyField(Categoria)

class Cliente(BaseModel):
    cpf = CharField(primary_key=True, max_length=14)
    nome = CharField(max_length=100)
    idade = IntegerField()
    email = CharField()
    senha = CharField()
    imagem = BlobField(null=True)
    telefone = CharField()
    #local = ForeignKeyField(Local)

class Estabelecimento(BaseModel):
    cnpj = CharField(primary_key=True, max_length=18)
    nome_ficticio = CharField(max_length=100)
    email = CharField()
    senha = CharField()
    imagem = BlobField(null=True)
    telefone = CharField()
    avaliacao = FloatField(null=True)
    qtd_visitas = IntegerField(default=0)
    operando = BooleanField(default=True)
    local = ForeignKeyField(Local)

#Contem os Pratos e Bebidas de um Estabelecimento
class Cardapio(BaseModel):
    pratos = ManyToManyField(Prato)
    bebidas = ManyToManyField(Bebida)
    estabelecimento = ForeignKeyField(Estabelecimento)

class Reserva(BaseModel):
    data_requisicao = DateTimeField()
    cliente = ForeignKeyField(Cliente)
    estabelecimento = ForeignKeyField(Estabelecimento)
    qtd_pessoas = IntegerField()
    data_marcada = CharField()
    horario_chegada = CharField()
    horario_saida = CharField()
    pratos = ManyToManyField(Prato)
    bebidas = ManyToManyField(Bebida)
    confirmacao = BooleanField(default=False)

class Agenda(BaseModel):
    dias = CharField()
    hora_inicio = CharField()
    hora_termino = CharField()
    qtd_lugares = IntegerField()
    lotacao_maxima_permetida = IntegerField()
    estabelecimento = ForeignKeyField(Estabelecimento)

class Notificacao(BaseModel):
    descricao = CharField()
    data_envio = DateTimeField()
    cliente = ForeignKeyField(Cliente)
    origem = CharField()
    lida = BooleanField(default=False)

class Ranking(BaseModel):
    pass