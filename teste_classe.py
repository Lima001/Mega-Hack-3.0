from funcionalidades.classes import *
from funcionalidades.seguranca import gerar_senha
from datetime import datetime

try:
    os.system("cls")

except:
    os.system("clear")

if os.path.exists(arquivo):
    os.remove(arquivo)

try:
    db.connect()
    db.create_tables([
        Cliente,
        Categoria,
        Prato,
        Bebida,
        Prato.categorias.get_through_model(),
        Bebida.categorias.get_through_model(),
        Estabelecimento,
        Agenda,
        Reserva,
        Notificacao
        ])

except OperationalError as err:
    print("ERRO !!!" + str (err))


cliente1 = Cliente.create(
    cpf="111.111.111-11",
    nome="Albertinho",
    idade=26,
    email="albertinho123@gmail.com",
    senha=gerar_senha("Minha#Super#Senha"),
    telefone="3333-1232"
)

cliente2 = Cliente.create(
    cpf="222.222.222-22",
    nome="Martinha Albelar",
    idade=22,
    email="MartusSpartusZ@gmail.com",
    senha=gerar_senha("#EraUmaVezUmaSenha"),
    telefone="99999-1232"
)


categoria1 = Categoria.create(nome="defumado")
categoria2 = Categoria.create(nome="frito")
categoria3 = Categoria.create(nome="tipico")
categoria4 = Categoria.create(nome="caseiro")
categoria5 = Categoria.create(nome="doce")
categoria6 = Categoria.create(nome="Alcool")


estabelecimento1 = Estabelecimento.create(
    cnpj = "42.318.949/0001-84",
    nome_ficticio = "BarzinDelusch",
    email = "BarzinDeluxe321@gmail.com",
    senha = gerar_senha("UmBarZinL@G@L"),
    telefone = "3332-1212",
    local = "Pommerland",
)
estabelecimento2 = Estabelecimento.create(
    cnpj = "45.128.959/1001-89",
    nome_ficticio = "ItaliCassiolla",
    email = "ItaliaC.Contato@gmail.com",
    senha = gerar_senha("#AlgumaFraseEmItaliano"),
    telefone = "99932-1522",
    local = "Pommerland",
    avaliacao = 9.5,
)

prato1 = Prato.create(
    nome="Pastel",
    preco=4.50,
    descricao="Pastel Gostoso e Cremoso",
    ingrediente="Massa de Pastel e Recheio de Carne",
    dia_periodo = "123456-3",
    estabelecimento = estabelecimento1
)

prato2 = Prato.create(
    nome="Bolinho de Carne",
    preco=3.50,
    dia_periodo = "123456-3",
    estabelecimento = estabelecimento1
)

prato3 = Prato.create(
    nome="Salmão Defunado Italiano",
    preco=50.00,
    descricao="Tradicional Prato Italiano com toque Brasileiro",
    dia_periodo = "246-13",
    avaliacao = 8,
    estabelecimento = estabelecimento2
)

prato1.categorias.add([categoria2,categoria4])
prato2.categorias.add(categoria2)
prato3.categorias.add([categoria1,categoria3,categoria4])


bebida1 = Bebida.create(
    nome="Toddy Radical",
    preco=2.50,
    descricao="600ml",
    dia_periodo = "123456-123",
    estabelecimento = estabelecimento1
)

bebida2 = Bebida.create(
    nome="Coquetel Italiano",
    preco=14.50,
    descricao="500ml",
    ingrediente="20ml de Puro Alcool",
    dia_periodo = "246-3",
    avaliacao = 5.0,
    estabelecimento = estabelecimento2
)

bebida1.categorias.add([categoria5])
bebida2.categorias.add([categoria5,categoria6])

#Agenda Restaurante 1
agenda1 = Agenda.create(
    dias = "1234567",
    hora_inicio ="17:30",
    hora_termino ="23:30",
    lotacao_maxima_permitida = 8,
    estabelecimento = estabelecimento1
)
#Agendas Restaurante 2
agenda2 = Agenda.create(
    dias = "12345",
    hora_inicio ="17:30",
    hora_termino ="23:30",
    lotacao_maxima_permitida = 28,
    estabelecimento = estabelecimento2
)

reserva1 = Reserva.create(
    data_requisicao = datetime.now(),
    cliente = cliente1,
    estabelecimento = estabelecimento1,
    qtd_pessoas = 1,
    data_marcada = "07/07/20",
    horario_chegada = "17:45",
    horario_saida = "20:30",
)

reserva2 = Reserva.create(
    data_requisicao = datetime.now(),
    cliente = cliente2,
    estabelecimento = estabelecimento2,
    qtd_pessoas = 4,
    data_marcada = "08/07/20",
    horario_chegada = "20:45",
    horario_saida = "21:45",
)

notificao1 = Notificacao.create(
    descricao = "ERRO POXA VIDA",
    data_envio = datetime.now(),
    cliente = cliente2,
    origem = "Sistema"
)