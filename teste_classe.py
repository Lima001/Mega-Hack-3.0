from classes import *


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
        Cardapio,
        Cardapio.pratos.get_through_model(),
        Cardapio.bebidas.get_through_model()
        ])

except OperationalError as err:
    print ( "ERRO !!!" +str (err))


cliente1 = Cliente.create(
    cpf="111.111.111-11",
    nome="Albertinho",
    idade=26,
    email="albertinho123@gmail.com",
    senha=gerar_senha("Minha#Super#Senha"),
    telefone="3333-1232",
)

cliente2 = Cliente.create(
    cpf="222.222.222-22",
    nome="Martinha Albelar",
    idade=22,
    email="MartusSpartusZ@gmail.com",
    senha=gerar_senha("#EraUmaVezUmaSenha"),
    telefone="99999-1232",
)


categoria1 = Categoria.create(nome="defumado")
categoria2 = Categoria.create(nome="frito")
categoria3 = Categoria.create(nome="típico")
categoria4 = Categoria.create(nome="caseiro")
categoria5 = Categoria.create(nome="doce")
categoria6 = Categoria.create(nome="Alcool")

prato1 = Prato.create(
    nome="Pastel",
    preco=4.50,
    descricao="Pastel Gostoso e Cremoso",
    ingrediente="Massa de Pastel e Recheio de Carne",
    dia_periodo = "123456-3"
)

prato2 = Prato.create(
    nome="Bolinho de Carne",
    preco=3.50,
    dia_periodo = "123456-3"
)

prato3 = Prato.create(
    nome="Salmão Defunado Italiano",
    preco=50.00,
    descricao="Tradicional Prato Italiano com toque Brasileiro",
    dia_periodo = "246-13"
)

prato1.categorias.add([categoria2,categoria4])
prato2.categorias.add(categoria2)
prato3.categorias.add([categoria1,categoria3,categoria4])

bebida1 = Bebida.create(
    nome="Toddy Radical",
    preco=2.50,
    descricao="600ml",
    dia_periodo = "123456-123"
)

bebida2 = Bebida.create(
    nome="Coquetel Italiano",
    preco=14.50,
    descricao="500ml",
    ingrediente="20ml de Puro Alcool",
    dia_periodo = "246-3"
)

bebida1.categorias.add([categoria5])
bebida2.categorias.add([categoria5,categoria6])

cardapio_restaurante1 = Cardapio.create()
cardapio_restaurante2 = Cardapio.create()

cardapio_restaurante1.pratos.add([prato1,prato2])
cardapio_restaurante1.bebidas.add(bebida1)
cardapio_restaurante2.pratos.add(prato3)
cardapio_restaurante2.bebidas.add(bebida2)