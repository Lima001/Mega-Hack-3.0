# Este modulo acrescenta funcionalidades de segurança que podem
# ser importadas e usadas na plataforma para verificar estabilidade dos dados

import hashlib
import re

#Necessita ser implementado
#Usar RegEx

def cpf_valido(cpf:str) -> bool:
    if len(cpf) < 14:
        return False
    
    lista = []
    for i in cpf:
        lista.append(i)

    lista.remove(".")
    lista.remove(".")
    lista.remove("-")

    # primeira etapa
    soma = 0
    cont = 10
    for i in range(0,len(lista)-2):
        soma += int(lista[i]) * cont
        cont -= 1

    resto1 = (soma*10) % 11
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
    pass

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

#Necessário implementar BD para testar função
def verificar_email(email:str, lista_email:object) -> bool:
    '''
    Verifica se o email informado está presente na base de dados (Objeto retornado pela Consulta Peewee)
    Retorna um valor Lógico True caso o email corresponda a lista de email salvos, 
    caso contrário retorna False
    '''
    for i in lista_email:
        if i == email:
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
    senha = cpf_valido(input("CPF: "))
    print("Hash:", senha)
