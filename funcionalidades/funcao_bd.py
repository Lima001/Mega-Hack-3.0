# Este modulo acrescenta funcionalidades para aplicar funções a base de dados
# Usado por exemplo para dar desconto em um prato de um estabelecimento

def descontar_preco(preco:float, porcentagem:float) -> float:
    '''
    Retorna um valor x gerado a partir do desconto de uma porcentagem sobre um valor de entrada
    '''
    return preco - preco* (porcentagem/100)