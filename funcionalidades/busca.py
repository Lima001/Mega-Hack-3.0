# Este modulo acrescenta funcionalidades de busca que podem
# ser importadas e usadas na plataforma para filtrar e refinar as pesquisas
# Ex: Ranking, Prato Mais Visto do Estabeleciemento etc...

if __name__ == "__main__":
    from classes import *
else:
    from funcionalidades.classes import *

import json
from playhouse.shortcuts import model_to_dict

#Busca e Filtro por estabelecimentos
def buscar_estabelecimento_por_nome(nome):
    nome = f"%{nome}%"
    resultado = Estabelecimento.select().where(Estabelecimento.nome_ficticio**nome)
    return resultado

def filtrar_estabelecimento_por_cidade(estabelecimentos, lista_cidade):
    resultado = []
    for i in estabelecimentos:
        if i.local in lista_cidade:
            resultado.append(i)
    return resultado

def filtrar_estabelecimento_por_avaliacao(estabelecimentos, nota_min=0, nota_max=10):
    resultado = []
    for i in estabelecimentos:
        if i.avaliacao is not None:
            if i.avaliacao >= nota_min and i.avaliacao <= nota_max:
                resultado.append(i)
    return resultado

def filtrar_estabelecimento_por_agenda(estabelecimentos, dias="1234567"):
    resultado = []
    dias = f"%{dias}%"
    agendas = Agenda.select().where(Agenda.estabelecimento.in_(estabelecimentos) & Agenda.dias**dias)
    for i in agendas:
        resultado.append(i.estabelecimento)
    return resultado

#Busca e filtro por Pratos e Bebidas
def buscar_prato_por_nome(nome):
    nome = f"%{nome}%"
    resultado = Prato.select().where(Prato.nome**nome)
    return resultado

def buscar_bebida_por_nome(nome):
    nome = f"%{nome}%"
    resultado = Bebida.select().where(Bebida.nome**nome)
    return list(resultado)

def filtrar_por_categoria(objetos, categorias):
    resultado = []
    for i in objetos:
        for j in i.categorias:
            if j.nome in categorias:
                resultado.append(i)
                break
    return resultado

def filtrar_por_avaliacao(objetos, nota_min=0, nota_max=10):
    resultado = []
    for i in objetos:
        if i.avaliacao is not None:
            if i.avaliacao >= nota_min and i.avaliacao <= nota_max:
                resultado.append(i)
    return resultado

def filtrar_por_preco(objetos, preco_min=0, preco_max=100000):
    resultado = []
    for i in objetos:
        if i.preco >= preco_min and i.preco <= preco_max:
            resultado.append(i)
    return resultado

if __name__ == "__main__":
    db.connect()
    
    #Isso aqui pode parecer confuso, mas acreditem... Eu entendo o que está acontecendo
    
    #Teste funções estabelecimento
    resultado = buscar_estabelecimento_por_nome("a") 
    print(resultado)
    for i in resultado:
        print(i.local)
    
    print(filtrar_estabelecimento_por_cidade(resultado,["Pommerland"]))
    print(filtrar_estabelecimento_por_avaliacao(resultado,5))
    print(filtrar_estabelecimento_por_agenda(resultado,"2"))

    print("-"*35)

    #Teste funções pratos
    resultado = buscar_prato_por_nome("a")
    print(resultado)
    for i in resultado:
        print(i.nome)
    
    print(filtrar_por_categoria(resultado,["frito","caseiro"]))
    print(filtrar_por_avaliacao(resultado,8))
    print(filtrar_por_preco(resultado,preco_max=5))

    print("-"*35)

    #Teste funções bebidas
    resultado = buscar_bebida_por_nome("a")
    print(resultado)
    for i in resultado:
        print(i.nome)
    
    print(filtrar_por_categoria(resultado,["Alcool","caseiro"]))
    print(filtrar_por_avaliacao(resultado,4.5))
    print(filtrar_por_preco(resultado,preco_max=5))