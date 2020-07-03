# Este modulo acrescenta funcionalidades de segurança que podem
# ser importadas e usadas na plataforma para verificar estabilidade dos dados

import hashlib
import re

#Acredito que ele não está funcionando corretamente... Temos que rever isso
def cpf_valido(cpf:str) -> bool:
    if len(cpf) < 14:
        return False
    
    lista = []
    for i in cpf:
        lista.append(i)
    try:
        lista.remove(".")
        lista.remove(".")
        lista.remove("-")
    except:
        pass
    # primeira etapa
    soma = 0
    cont = 10
    for i in range(0,len(lista)-2):
        soma += int(lista[i]) * cont
        cont -= 1

    resto1 = (soma*10) % 11
    if resto1 == 10:
        resto1 = 0
    
    digito1 = False
    if resto1 == int(lista[-2]):
        digito1 = True


    # segunda etapa
    soma = 0
    cont = 11
    for i in range(0,len(lista)-1):
        soma += int(lista[i]) * cont
        cont -= 1

    resto2 = (soma*10) % 11
    digito2 = False
    if resto2 == int(lista[-1]):
        digito2 = True

    if digito1 == True and digito2 == True:
        return True   
    else: 
        return False



def cnpj_valido(cnpj:str) -> bool:
    lista = []
    for i in cnpj:
        lista.append(i)


    try:
        lista.remove(".")
        lista.remove(".")
        lista.remove("/")
        lista.remove("-")
    except:
        pass 

    # primeira etapa
    soma = 0
    cont = 6
    for i in range(0,len(lista)-2):
        cont -= 1
        soma += int(lista[i]) * cont
        if cont == 2:
            cont = 10

    resto = soma % 11
    if resto < 2:
        resto = 0
    else:
        resto = 11 - resto

    digito1 = False
    if resto == int(lista[-2]):
        digito1 = True


    soma = 0
    cont = 7
    for i in range(0,len(lista)-1):
        cont -= 1
        soma += int(lista[i]) * cont
        if cont == 2:
            cont = 10

    resto = soma % 11
    if resto < 2:
        resto = 0
    else:
        resto = 11 - resto

    digito2 = False
    if resto == int(lista[-1]):
        digito2 = True

    if digito1 == True and digito2 == True:
        return True   
    else: 
        return False

def email_valido(email:str) -> bool: 
    '''
    Verifica se a cadeia de caracteres passada como entrada
    consiste em um formato válido do tipo ...@gmail.com
    Retorna o valor lógico True em caso de sucesso, e 
    False em caso de erro  
    '''
    padrao = "^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w+$"
    if re.search(padrao, email):
        return True
    return False

def gerar_senha(senha:str) -> str: #Testada e funcional
    '''
    Retorna o hash da senha passada como entrada para eventual gravação na base de dados
    '''
    gerador = hashlib.sha512()
    gerador.update(senha.encode("utf-8"))
    return gerador.hexdigest()

def verificar_senha(senha:str, padrao_hash:str) -> bool: #Testada e Funcional
    '''
    Verifica se a senha informada confere com o hash passado (Pegar hash da base de dados)

    Retorna True caso sejam compatíveis, caso contrário retorna False
    '''
    senha = gerar_senha(senha)
    return senha == padrao_hash

if __name__ == "__main__":
    from classes import *

    db.connect()

    #Teste encriptar Senha
    #Esperado: Uma senha ilegivel (Um hash)
    minha_senha = "#MuitoDificilH@H@"
    padrao_hash = gerar_senha(minha_senha)
    print("1º Teste: ", padrao_hash, end="\n"*2)

    #Teste verificar se Senha bate
    #Esperado: True
    print("2º Teste: ", verificar_senha(minha_senha, padrao_hash), end="\n"*2)

    #Verificar se o email esta em formato valido
    #Esperado: Depende conforme entrada (True or False)
    seu_email = input("Digite um email valido: ")
    print("3º Teste: ", email_valido(seu_email), end="\n"*2)

    #Verificar cpf valido
    #Esperado: Depende da entrada
    #Valor de Teste 272.396.372-12 - Esperado True
    print("4º Teste Valor Pré-definido: ", cpf_valido("272.396.372-12"))
    seu_cpf = input("Digite um cpf valido: ")
    print("5º Teste: ", cpf_valido(seu_cpf), end="\n"*2)
