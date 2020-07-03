# Este modulo acrescenta funcionalidades para gerenciar o Banco de Dados
# Usado para performar CRUD na base de dados

from seguranca import *
from classes import *

#Funções para Cliente
def salvar_cliente(dados):
    cpf = dados["cpf"]
    email = dados["email"]
    
    if not(cpf_valido(cpf) and email_valido(email)):
        return False
    
    nome = dados["nome"]
    senha = gerar_senha(dados["senha"])
    telefone = dados["telefone"]
    imagem = dados["imagem"] 
    idade = dados["idade"]
    
    try:
        cliente = Cliente.create(
            cpf = cpf,
            nome = nome,
            email = email,
            senha = senha,
            telefone = telefone,
            imagem = imagem,
            idade = idade
        )
        return True
    except:
        return False

def localizar_cliente(senha, email):
    try:
        cliente = Cliente.select().where(Cliente.email==email)[0]
    except:
        return False

    if verificar_senha(senha,cliente.senha):
        return True
    return False

def excluir_cliente(cpf):
    try:
        Cliente.delete().where(Cliente.cpf==cpf).execute()
        return True
    except:
        return False

#Funções para Estabelecimento
def salvar_estabelecimento(dados):
    cnpj = dados["cnpj"]
    email = dados["email"]

    if not(cnpj_valido(cnpj) and email_valido(email)):
        return False

    senha = gerar_senha(dados["senha"])
    nome_ficticio = dados["nome_ficticio"].lower()
    telefone = dados["telefone"]
    local = dados["local"].lower()
    imagem = dados["imagem"]
    avaliacao = dados["avaliacao"]  

    try:
        Estabelecimento.create(
            cnpj = cnpj,
            email = email,
            senha = senha,
            nome_ficticio = nome_ficticio,
            telefone = telefone,
            local = local,
            imagem = imagem,
            avaliacao = avaliacao
        )
        return True
    except:
        return False

def localizar_estabelecimento(email, senha):
    try:
        estabelecimento = Estabelecimento.select().where(Estabelecimento.email==email)[0]
    except:
        return False

    if verificar_senha(senha,estabelecimento.senha):
        return True
    return False

def excluir_estabelecimento(cnpj):
    try:
        Estabelecimento.delete().where(Estabelecimento.cnpj==cnpj).execute()
        return True
    except:
        return False

#Funções para Prato
def salvar_prato(dados):
    nome = dados["nome"]
    preco = dados["preco"]
    imagem = dados["imagem"]
    descricao = dados["descricao"]
    ingredientes = dados["ingredientes"]
    dia_periodo = dados["dia_periodo"]
    avaliacao = dados["avaliacao"]
    categorias = dados["categorias"]
    estabelecimento = dados["estabelecimento"]

    try:
        prato_criado = Prato.create(
            nome = nome,
            preco = preco,
            imagem = imagem,
            descricao = descricao,
            ingredientes = ingredientes,
            dia_periodo = dia_periodo,
            avaliacao = avaliacao,
            estabelecimento = estabelecimento
        )
        categorias_bd = []
        for i in categorias:
            try:
                novo = Categoria.create(nome=i)
                categorias_bd.append(novo)
            except:
                velho = Categoria.select().where(Categoria.nome==i)[0]
                categorias_bd.append(velho)
        
        prato_criado.categorias.add(categorias_bd)
        return True
    except:
        return False

def excluir_prato(id):
    try:
        prato = Prato.get(Prato.id==id)
        prato.delete_instance(recursive=True)
        return True
    except:
        return False

#Funções para Bebida
def salvar_bebida(dados):
    nome = dados["nome"]
    preco = dados["preco"]
    imagem = dados["imagem"]
    descricao = dados["descricao"]
    ingredientes = dados["ingredientes"]
    dia_periodo = dados["dia_periodo"]
    avaliacao = dados["avaliacao"]
    categorias = dados["categorias"]
    estabelecimento = dados["estabelecimento"]

    try:
        bebida_criado = Bebida.create(
            nome = nome,
            preco = preco,
            imagem = imagem,
            descricao = descricao,
            ingredientes = ingredientes,
            dia_periodo = dia_periodo,
            avaliacao = avaliacao,
            estabelecimento = estabelecimento
        )
        categorias_bd = []
        for i in categorias:
            try:
                novo = Categoria.create(nome=i)
                categorias_bd.append(novo)
            except:
                velho = Categoria.select().where(Categoria.nome==i)[0]
                categorias_bd.append(velho)
        
        bebida_criado.categorias.add(categorias_bd)
        return True
    except:
        return False

def excluir_bebida(id):
    try:
        bebida = Bebida.get(Bebida.id==id)
        bebida.delete_instance(recursive=True)
        return True
    except:
        return False

if __name__ == "__main__":
    db.connect()

    dados = {
        "nome":"Gabriel Lima",
        "senha":"123Senha123", 
        "telefone":"3333-1212",
        "cpf":"723.114.194-39",
        "email":"lima123@gmaial.com",
        "imagem":None,
        "idade":None}
    
    print(salvar_cliente(dados))
    print(localizar_cliente("123Senha123","lima123@gmaial.com"))
    print(excluir_cliente("723.114.194-39"))

    print("-"*10)

    dados = {
            "cnpj": "65.545.322/0001-61",
            "email": "efood@gmail.com",
            "senha": "SuperBlasterFood",
            "nome_ficticio": "EFOOD",
            "telefone": "3332-1232",
            "local": "Pommerland",
            "imagem": None,
            "avaliacao": None}

    print(salvar_estabelecimento(dados))
    print(localizar_estabelecimento("efood@gmail.com","SuperBlasterFood"))
    print(excluir_estabelecimento("65.545.322/0001-61"))

    print("-"*10)

    dados = {
        "nome": "Almondega Suiça",
        "preco": 12.50,
        "imagem": None,
        "descricao": None,
        "ingredientes": None,
        "dia_periodo": "123-123",
        "avaliacao": 8.0,
        "categorias": ["frito","tradicional"],
        "estabelecimento": Estabelecimento.select().where(Estabelecimento.cnpj=="45.128.959/1001-89")[0]        
    }
    print(salvar_prato(dados))
    id = Prato.select(Prato.id).where(Prato.nome=="Almondega Suiça")[0]
    print(excluir_prato(id))

    print("-"*10)

    dados = {
        "nome": "Super Bomba de Chocolate Cremoso",
        "preco": 12.50,
        "imagem": None,
        "descricao": None,
        "ingredientes": None,
        "dia_periodo": "123-123",
        "avaliacao": 8.0,
        "categorias": ["cremoso","chocolate"],
        "estabelecimento": Estabelecimento.select().where(Estabelecimento.cnpj=="45.128.959/1001-89")[0]        
    }
    print(salvar_bebida(dados))
    id = Bebida.select(Bebida.id).where(Bebida.nome=="Super Bomba de Chocolate Cremoso")[0]
    print(excluir_bebida(id))