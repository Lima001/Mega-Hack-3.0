# Este modulo acrescenta funcionalidades de busca que podem
# ser importadas e usadas na plataforma para filtrar e refinar as pesquisas
# Ex: Ranking, Prato Mais Visto do Estabeleciemento etc...

def buscar_estabelecimento_por_nome(nome):
    nome = f"%{nome}%"
    return Estabelecimento.select.where(Estabelecimento.nome_ficticio**nome)

def filtrar():
    pass