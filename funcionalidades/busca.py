# Este modulo acrescenta funcionalidades de busca que podem
# ser importadas e usadas na plataforma para filtrar e refinar as pesquisas
# Ex: Ranking, Prato Mais Visto do Estabeleciemento etc...

from classes import *

def buscar_estabelecimento_por_nome(nome):
    nome = f"%{nome}%"
    return Estabelecimento.select().where(Estabelecimento.nome_ficticio**nome)

def filtrar():
    pass

if __name__ == "__main__":
    db.connect()
    #Esperado: 1 Objeto
    resultado = buscar_estabelecimento_por_nome("BarzinDelusch")
    for i in resultado:
        #Esperado: Nome dos Estabelecimentos
        print(i.nome_ficticio)

    print("-"*10)

    #Esperado: 2 Objeto
    resultado = buscar_estabelecimento_por_nome("a")
    for i in resultado:
        #Esperado: Nome dos Estabelecimentos
        print(i.nome_ficticio)